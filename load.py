from mysql.connector import connect, Error
import pandas as pd

def load_to_mysql(df, host='localhost', port=3306, user='root', password='yourpassword', database='etl_pipeline'):
    """
    Load cleaned DataFrame into MySQL using upsert pattern (idempotent).
    """
    if df.empty:
        print("✗ No data to load")
        return
    
    try:
        conn = connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO crypto_prices 
        (coin_name, price_usd, market_cap_usd, volume_24h_usd, fetched_at)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            price_usd = VALUES(price_usd),
            market_cap_usd = VALUES(market_cap_usd),
            volume_24h_usd = VALUES(volume_24h_usd),
            fetched_at = VALUES(fetched_at);
        """
        
        inserted = 0
        for _, row in df.iterrows():
            try:
                cursor.execute(insert_query, (
                    row['coin_name'],
                    float(row['price_usd']),
                    float(row['market_cap_usd']) if pd.notna(row['market_cap_usd']) else None,
                    float(row['volume_24h_usd']) if pd.notna(row['volume_24h_usd']) else None,
                    row['fetched_at']
                ))
                inserted += 1
            except Error as e:
                print(f"✗ Error inserting {row['coin_name']}: {e}")
        
        conn.commit()
        print(f"✓ Loaded {inserted}/{len(df)} rows to MySQL")
        
    except Error as e:
        print(f"✗ MySQL Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    from extract import extract_crypto_data
    from transform import transform_crypto_data
    
    raw_data = extract_crypto_data()
    df = transform_crypto_data(raw_data)
    load_to_mysql(df)