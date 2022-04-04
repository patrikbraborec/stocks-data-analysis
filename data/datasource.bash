curl http://localhost:3000/api/entities/dataSources \
  -H "Content-Type: application/vnd.gooddata.api+json" \
  -H "Accept: application/vnd.gooddata.api+json" \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -X POST \
  -d '{
      "data": {
          "attributes": {
              "name": "stocks-data",
              "url": "jdbc:postgresql://stocks-data-analysis-database:5432/stocks_data_analysis",
              "schema": "public",
              "type": "POSTGRESQL",
              "username": "admin",
              "password": "admin123"
          },
          "id": "stocks-data",
          "type": "dataSource"
      }
  }' | jq .
