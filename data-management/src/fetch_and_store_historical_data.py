import http.client
from decouple import config
import psycopg2
import json


def get_api_uri(stock):
    return f"/query?function=TIME_SERIES_DAILY&symbol={stock}&datatype=json"


def load_stocks_data():
    https_conn = http.client.HTTPSConnection(config('API_HTTPS_CONNECTION'))
    headers = {
        'X-RapidAPI-Host': config('API_HOST'),
        'X-RapidAPI-Key': config('API_KEY')
    }
    stocks = ['GTLB', 'RKLB']
    fetched_data = []

    for stock in stocks:
        https_conn.request(
            'GET',
            get_api_uri(stock),
            headers=headers
        )
        res = https_conn.getresponse()
        data = res.read().decode()
        fetched_data.append(json.loads(data))

    return fetched_data


def get_symbols(stocks_data):
    symbols = []

    for data in stocks_data:
        symbols.append(data['Meta Data']['2. Symbol'])

    return symbols


def get_time_series(stocks_data):
    time_series = []

    for data in stocks_data:
        time_series.append(data['Time Series (Daily)'])

    return time_series


def map_data_to_database_model(symbols, time_series):
    normalized_data = []
    for index, stock_data in enumerate(time_series):
        for date in stock_data:
            normalized_data.append({
                'symbol': symbols[index],
                'date': date,
                'open': stock_data[date]['1. open'],
                'high': stock_data[date]['2. high'],
                'low': stock_data[date]['3. low'],
                'close': stock_data[date]['4. close'],
                'volume': stock_data[date]['5. volume']
            })
    return normalized_data


def store_data():
    database_conn = psycopg2.connect(
        host=config('DATABASE_HOST'),
        database=config('DATABASE_NAME'),
        user=config('DATABASE_USER'),
        password=config('DATABASE_PASSWORD')
    )
    database_conn.autocommit = True
    cur = database_conn.cursor()
    stocks_data = load_stocks_data()
    symbols = get_symbols(stocks_data)
    time_series = get_time_series(stocks_data)
    data = map_data_to_database_model(symbols, time_series)
    for item in data:
        keys = item.keys()
        columns = ','.join(keys)
        values = ','.join(['%({})s'.format(k) for k in keys])
        insert = 'insert into historical_stocks ({0}) values ({1})'.format(columns, values)
        cur.execute(cur.mogrify(insert, item), item)
    cur.close()
