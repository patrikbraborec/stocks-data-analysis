import http.client
from decouple import config

conn = http.client.HTTPSConnection(config('API_HTTPS_CONNECTION'))

headers = {
    'X-RapidAPI-Host': config('API_HOST'),
    'X-RapidAPI-Key': config('API_KEY')
}

conn.request(
    'GET',
    '/query?interval=5min&function=TIME_SERIES_INTRADAY&symbol=MSFT&datatype=json&output_size=compact',
    headers=headers
)

res = conn.getresponse()
data = res.read().decode()

print(data)
