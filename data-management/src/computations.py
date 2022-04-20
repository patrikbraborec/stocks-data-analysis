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
            first_metric=f"metric/{metric_name}"
        )
    )
    indexed_df = indexed_df['first_metric'].to_frame()
    indexed_df[f"{metric_name}_sma30"] = indexed_df['first_metric'].rolling(30).mean()
    indexed_df[f"{metric_name}_cma"] = indexed_df['first_metric'].expanding().mean()
    indexed_df[f"{metric_name}_ema30"] = indexed_df['first_metric'].ewm(span=30).mean()
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
        insert = 'INSERT INTO stocks_technical_analysis (symbol, date, sma30, cma, ema30) VALUES (\'{0}\',\'{1}\',{2}, {3}, {4})'.format(
            stock_symbol, index.date(), row[f"{metric_name}_sma30"], row[f"{metric_name}_cma"],
            row[f"{metric_name}_ema30"])
        cur.execute(insert)
    cur.close()


def compute():
    gp = GoodPandas(host, token)
    frames = gp.data_frames(workspace_id)
    gtlb_indexed_df = compute_sma('gtlb_close', frames)
    store_sma(gtlb_indexed_df, 'GTLB', 'gtlb_close')
