# https://api.binance.com/api/v1/ticker/price?symbol=XRPETH

import urllib.request, json

def get_binance_time():
    # Set variable time to JSON output of server time from Binance API
    with urllib.request.urlopen("https://api.binance.com/api/v1/time") as url:
        time_json = json.loads(url.read().decode())
        # Filter time from dictionary in time_json
        time = time_json.get("serverTime")
        # Return unix time (with milliseconds)
        return time

def get_binance_all_prices():
    # Set variable price to JSON output of all prices from Binance API
    # JSON output consists of dictionaries in list
    with urllib.request.urlopen("https://api.binance.com/api/v1/ticker/price") as url:
        prices = json.loads(url.read().decode())
        # Return JSON output (list consisting of multiple dictionaries)
        return prices

def save_to_json(filename, content):
    # Save content into filename
    with open(filename, "w") as file:
        json.dump(content, file)

def read_from_json(filename):
    # Read from file
    with open(filename, "r") as file:
        content = json.load(file)
        return content

def get_symbol(all_prices, symbol):
    # Filter specific symbol dictionary from variable all_prices (function get_binance_all_prices())
    filtered = list(filter(lambda price: price["symbol"] == symbol, all_prices))
    # Get value from price key from variable filtered
    name = filtered[0].get("symbol")
    price = filtered[0].get("price")
    # Return filtered symbol in tuple consisting of name and price
    return name, price

# # Example usage

# # Set variable all_prices to function get_binance_all_prices() to reduce amount of requests to Binance API
# all_prices = get_binance_all_prices()
# # Print tuple
# print(get_symbol(all_prices, "XRPETH"))
# # Print tuple[0] for name of symbol
# print(get_symbol(all_prices, "XRPETH")[0])
# # Print tuple[1] for price of symbol
# print(get_symbol(all_prices, "XRPETH")[1])