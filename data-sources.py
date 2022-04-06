import gooddata_sdk
from decouple import config
from gooddata_sdk import CatalogDataSourcePostgres, PostgresAttributes, BasicCredentials

host = config('GOODDATA_HOST')
token = config('GOODDATA_API_TOKEN')

sdk = gooddata_sdk.GoodDataSdk.create(host, token)

sdk.catalog_data_source.create_or_update_data_source(
    CatalogDataSourcePostgres(
        id="stocks-data",
        name="stocks-data",
        db_specific_attributes=PostgresAttributes(
            host="localhost", db_name="stocks_data_analysis"
        ),
        schema="public",
        credentials=BasicCredentials(
            username=config('DATABASE_USER'),
            password=config('DATABASE_PASSWORD'),
        ),
        enable_caching=False,
        url_params=[("param", "value")]
    )
)
