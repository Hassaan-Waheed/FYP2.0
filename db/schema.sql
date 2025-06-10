-- Assets table
CREATE TABLE asset (
    id VARCHAR PRIMARY KEY,
    symbol VARCHAR NOT NULL,
    name VARCHAR NOT NULL
);

-- OHLCV table
CREATE TABLE ohlcv (
    asset_id VARCHAR REFERENCES asset(id),
    timestamp TIMESTAMPTZ,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT,
    PRIMARY KEY (asset_id, timestamp)
);

-- Tokenomics features
CREATE TABLE tokenomics_features (
    asset_id VARCHAR REFERENCES asset(id),
    date DATE,
    tvl_ratio FLOAT,
    weekly_active_wallets INT,
    dev_commit_activity INT,
    wallet_concentration FLOAT,
    unlock_volume FLOAT,
    fdv_ratio FLOAT,
    avg_daily_volume FLOAT,
    PRIMARY KEY (asset_id, date)
);

-- Technical features
CREATE TABLE technical_features (
    asset_id VARCHAR REFERENCES asset(id),
    date DATE,
    ma_50 FLOAT,
    ma_200 FLOAT,
    ma_crossover BOOLEAN,
    rsi_14 FLOAT,
    macd_hist FLOAT,
    bb_width FLOAT,
    obv FLOAT,
    PRIMARY KEY (asset_id, date)
);

-- Sentiment features
CREATE TABLE sentiment_features (
    asset_id VARCHAR REFERENCES asset(id),
    date DATE,
    finbert_polarity FLOAT,
    sentiment_volatility FLOAT,
    news_freq INT,
    social_mentions INT,
    yt_growth FLOAT,
    PRIMARY KEY (asset_id, date)
); 