DELETE FROM historical_stocks;
DELETE FROM stocks_technical_analysis;
ALTER SEQUENCE historical_stocks_id_seq RESTART WITH 1;
ALTER SEQUENCE stocks_technical_analysis_id_seq RESTART WITH 1;