-- ==============================================================================
-- Challenge 10: Ingest Real-Time Financial Data into Tiger Cloud
-- Hypertable & 1-Minute OHLCV (Open-High-Low-Close-Volume) Candlesticks
-- ==============================================================================

-- 1. Create table for high-frequency financial trade execution ticks
CREATE TABLE IF NOT EXISTS market_trade_ticks (
    trade_time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(16) NOT NULL,
    price NUMERIC(16, 4) NOT NULL,
    quantity NUMERIC(16, 6) NOT NULL,
    trade_side VARCHAR(4) NOT NULL,    -- 'BUY' or 'SELL'
    exchange VARCHAR(16) DEFAULT 'BINANCE',
    trade_id VARCHAR(32)
);

-- 2. Convert to TimescaleDB Hypertable partitioned on trade_time
SELECT create_hypertable(
    'market_trade_ticks',
    'trade_time',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

-- 3. Create index for fast symbol-specific candlestick queries
CREATE INDEX IF NOT EXISTS idx_market_ticks_symbol_time 
ON market_trade_ticks (symbol, trade_time DESC);

-- 4. Create 1-Minute Candlestick (OHLCV) Continuous Aggregate
CREATE MATERIALIZED VIEW IF NOT EXISTS ohlcv_1m_cagg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 minute', trade_time) AS candle_bucket,
    symbol,
    COUNT(*) AS total_trades,
    ROUND(FIRST(price, trade_time)::numeric, 2) AS open_price,
    ROUND(MAX(price)::numeric, 2) AS high_price,
    ROUND(MIN(price)::numeric, 2) AS low_price,
    ROUND(LAST(price, trade_time)::numeric, 2) AS close_price,
    ROUND(SUM(quantity)::numeric, 4) AS volume,
    ROUND(SUM(price * quantity)::numeric, 2) AS quote_volume
FROM market_trade_ticks
GROUP BY candle_bucket, symbol
WITH NO DATA;

-- 5. Verification
SELECT hypertable_name, num_dimensions 
FROM timescaledb_information.hypertables 
WHERE hypertable_name = 'market_trade_ticks';
