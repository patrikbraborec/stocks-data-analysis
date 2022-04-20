from argparse import ArgumentParser
import data_sources
import fetch_and_store_historical_data
import computations

parser = ArgumentParser()
parser.add_argument(
    "-d", "--datasource",
    help="connect data source (PostgreSQL) to GoodData.CN",
    default=False
)
parser.add_argument(
    "-s", "--store-data",
    help="fetch and store data to PostgreSQL",
    default=False
)
parser.add_argument(
    "-c", "--compute",
    help="compute new metrics",
    default=False
)
args = vars(parser.parse_args())
datasource_flag = args['datasource']
store_data_flag = args['store_data']
compute_flag = args['compute']


def main():
    if datasource_flag:
        data_sources.connect_postgres()
        print('Datasource connected')

    if store_data_flag:
        fetch_and_store_historical_data.store_data()
        print('Data stored')

    if compute_flag:
        computations.compute()
        print('Data computed and stored')


main()
