SELECT 'CREATE DATABASE stocks_data_analysis'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stocks_data_analysis')\gexec

CREATE TABLE IF NOT EXISTS historical_stocks (
    id serial,
    symbol varchar not null,
    date date not null,
    open decimal not null,
    high decimal not null,
    low decimal not null,
    close decimal not null,
    volume decimal not null
);

CREATE TABLE IF NOT EXISTS stocks_technical_analysis (
    id serial,
    symbol varchar not null,
    date date not null,
    sma5 decimal not null
);