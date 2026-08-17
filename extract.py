import requests
import json
from datetime import datetime
from pathlib import Path

def extract_crypto_data(coins=['bitcoin', 'ethereum', 'cardano', 'solana'], save_raw=True):
    """
    Fetch crypto price data from CoinGecko API.
    
    Args:
        coins: List of coin IDs to fetch
        save_raw: Whether to save raw JSON to raw/ folder (for debugging)
    
    Returns:
        dict: Raw JSON response from API
    """
    coin_ids = ','.join(coins)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if save_raw:
            Path('raw').mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_file = f'raw/crypto_raw_{timestamp}.json'
            with open(raw_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Raw data saved to {raw_file}")
        
        print(f"✓ Fetched data for {len(data)} coins")
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data: {e}")
        raise

if __name__ == '__main__':
    raw_data = extract_crypto_data()
    print(json.dumps(raw_data, indent=2))