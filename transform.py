import pandas as pd
from datetime import datetime

def transform_crypto_data(raw_data):
    """
    Transform raw CoinGecko JSON into a clean DataFrame.
    """
    records = []
    
    for coin_name, prices in raw_data.items():
        record = {
            'coin_name': coin_name,
            'price_usd': prices.get('usd'),
            'market_cap_usd': prices.get('usd_market_cap'),
            'volume_24h_usd': prices.get('usd_24h_vol'),
            'fetched_at': datetime.now()
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    
    print(f"Before cleaning: {len(df)} rows")
    
    df = df.dropna(subset=['price_usd'])
    print(f"After removing null prices: {len(df)} rows")
    
    df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')
    df['market_cap_usd'] = pd.to_numeric(df['market_cap_usd'], errors='coerce')
    df['volume_24h_usd'] = pd.to_numeric(df['volume_24h_usd'], errors='coerce')
    
    df = df.drop_duplicates(subset=['coin_name'])
    print(f"After dedup: {len(df)} rows")
    
    print(f"✓ Transformation complete")
    return df

if __name__ == '__main__':
    from extract import extract_crypto_data
    raw_data = extract_crypto_data()
    df = transform_crypto_data(raw_data)
    print(df)