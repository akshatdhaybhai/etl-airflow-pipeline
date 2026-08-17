from extract import extract_crypto_data
from transform import transform_crypto_data
from load import load_to_mysql

if __name__ == '__main__':
    print("=" * 50)
    print("ETL PIPELINE START")
    print("=" * 50)
    
    print("\n[EXTRACT] Fetching data from API...")
    raw_data = extract_crypto_data()
    
    print("\n[TRANSFORM] Cleaning data...")
    df = transform_crypto_data(raw_data)
    
    print("\n[LOAD] Writing to MySQL...")
    load_to_mysql(df)
    
    print("\n" + "=" * 50)
    print("✓ PIPELINE COMPLETE")
    print("=" * 50)