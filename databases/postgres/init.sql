CREATE TABLE symbols_rate (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(3) UNIQUE,
    rate REAL
);

INSERT INTO symbols_rate (symbol, rate) VALUES ('USD', '1');