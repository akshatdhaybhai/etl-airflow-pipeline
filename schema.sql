-- ETL Pipeline Schema
-- Design Decisions:
-- 1. Single table (crypto_prices) for simplicity
-- 2. DECIMAL for prices (exact, not float)
-- 3. UNIQUE KEY on (coin_name) to prevent duplicates for each coin
-- 4. Using INSERT ... ON DUPLICATE KEY UPDATE for idempotency

DROP TABLE IF EXISTS crypto_prices;

CREATE TABLE crypto_prices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    coin_name VARCHAR(50) NOT NULL,
    price_usd DECIMAL(15, 2) NOT NULL,
    market_cap_usd DECIMAL(20, 2),
    volume_24h_usd DECIMAL(20, 2),
    fetched_at DATETIME NOT NULL,
    UNIQUE KEY unique_coin (coin_name)
);