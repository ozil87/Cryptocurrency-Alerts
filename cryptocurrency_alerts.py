from binance_api import get_binance_time, get_binance_all_prices, get_symbol, save_to_json, read_from_json
import time

def main():
    # Set variable symbols to list of desired symbols
    symbols = ["XRPETH", "NEOETH"]

    # Set variable time to current server time from Binance API
    current_server_time = get_binance_time()

    # Set variable last_prices to prices from prices.txt
    last_prices = read_from_json("prices.txt")

    # Set variable all_prices to prices from Binance API
    all_prices = get_binance_all_prices()

    # Save all_prices into prices.txt
    save_to_json("prices.txt", all_prices)

    # Print current server time from Binance API
    print(f"The server time from the Binance API is currently {current_server_time}.")

    # Iterate through each symbol in list symbols
    for symbol in symbols:
        # Set variable symbol_name to tuple[0] for name of symbol
        symbol_name = get_symbol(all_prices, symbol)[0]
        # Set variable symbol_price to tuple[1] for price of symbol
        symbol_price = get_symbol(all_prices, symbol)[1]

        # Check if variable last_prices exists
        if last_prices:
            # Set variable last_symbol_name to tuple[0] for name of symbol
            last_symbol_name = get_symbol(last_prices, symbol)[0]
            # Set variable last_symbol_price to tuple[1] for price of symbol
            last_symbol_price = get_symbol(last_prices, symbol)[1]

            # Check if last_symbol_price is equal to symbol_price
            if last_symbol_name == symbol_name and last_symbol_price == symbol_price:
                # Print last_symbol_price and symbol_price is equal
                print(f"The price for {symbol_name} is the same as its previous price and is currently {symbol_price}.")
            
            # Check if last_symbol_price is less than symbol_price
            elif last_symbol_name == symbol_name and last_symbol_price < symbol_price:
                # Print last_symbol_price is less than symbol_price
                print(f"The price for {symbol_name} is up from its previous price of {last_symbol_price} and is currently {symbol_price}.")

            # Check if last_symbol_price is greater than symbol_price
            elif last_symbol_name == symbol_name and last_symbol_price > symbol_price:
                # Print last_symbol_price is greater than symbol_price
                print(f"The price for {symbol_name} is down from its previous price of {last_symbol_price} and is currently {symbol_price}.")

        # If variable last_prices does not exist
        else:
                # Print symbol name and symbol price
                print(f"The price for {symbol_name} is currently {symbol_price}.")

if __name__ == "__main__":
    save_to_json("prices.txt", None)
    # Loop function main()
    while True:
        # Execute function main()
        main()
        # Wait x seconds until executing function main()
        time.sleep(10)