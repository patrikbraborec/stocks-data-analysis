from gooddata_pandas import GoodPandas
from decouple import config
import psycopg2

host = config('GOODDATA_HOST')
token = config('GOODDATA_API_TOKEN')
workspace_id = config('GOODDATA_WORKSPACE_ID')


def compute_sma(metric_name, frames):
    indexed_df = frames.indexed(
        index_by='label/date.day',
        columns=dict(
            first_label='label/historical_stocks.symbol',
            first_metric='metric/' + metric_name
        )
    )
    indexed_df = indexed_df['first_metric'].to_frame()
    indexed_df[metric_name + '_sma5'] = indexed_df['first_metric'].rolling(5).mean()
    indexed_df.dropna(inplace=True)
    return indexed_df


def store_sma(indexed_df, stock_symbol, metric_name):
    database_conn = psycopg2.connect(
        host='localhost',
        database='stocks_data_analysis',
        user=config('DATABASE_USER'),
        password=config('DATABASE_PASSWORD')
    )
    database_conn.autocommit = True
    cur = database_conn.cursor()
    for index, row in indexed_df.iterrows():
        insert = 'INSERT INTO stocks_technical_analysis (symbol, date, sma5) VALUES (\'{0}\',\'{1}\',{2})'.format(stock_symbol, index.date(), row[metric_name + '_sma5'])
        cur.execute(insert)
    cur.close()


def compute():
    gp = GoodPandas(host, token)
    frames = gp.data_frames(workspace_id)
    gtlb_indexed_df = compute_sma('gtlb_close', frames)
    store_sma(gtlb_indexed_df, 'GTLB', 'gtlb_close')

    print("Done")


compute()