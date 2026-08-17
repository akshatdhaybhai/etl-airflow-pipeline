import requests
import json

# Fetch data from CoinGecko API
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true"

response = requests.get(url)
data = response.json()

# Print the raw JSON response
print(json.dumps(data, indent=2))