import gooddata_sdk
from decouple import config
from gooddata_sdk import CatalogDataSource, PostgresAttributes, BasicCredentials

host = config('GOODDATA_HOST')
token = config('GOODDATA_API_TOKEN')

sdk = gooddata_sdk.GoodDataSdk.create(host, token)

sdk.catalog_data_source.create_or_update_data_source(
    CatalogDataSource(
        id="stocks-data",
        name="stocks-data",
        url="jdbc:postgresql://stocks-data-analysis-database:5432/stocks_data_analysis",
        schema="public",
        credentials=BasicCredentials(
            username=config('DATABASE_USER'),
            password=config('DATABASE_PASSWORD'),
        ),
        enable_caching=False,
        url_params=[("param", "value")],
        data_source_type='POSTGRESQL'
    )
)