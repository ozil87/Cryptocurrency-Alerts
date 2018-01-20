from binance_api import get_binance_time, get_binance_all_prices, get_symbol, save_to_json, read_from_json
import time

def get_user_symbols(filename):
    with open(filename, "r") as file:
        content = file.read().splitlines()
        file.close()
    return content

def save_user_symbols(filename, symbols):
    with open(filename, "w") as file:
        for symbol in symbols:
            file.write(f"{symbol}\n")
        file.close()


def main():
    # Set variable symbols to list of desired symbols
    symbols = get_user_symbols("symbols.txt")

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
    # Set prices.txt to ""
    save_to_json("prices.txt", "")
    # Create symbols.txt is does not exist
    with open("symbols.txt", "w+") as file:
        file.write("")
        file.close()

    while True:
        # Menu
        user_input = str(input("[0] Begin monitoring prices\n[1] Select symbol pairings to monitor\n"))

        # Option 1: Start monitoring
        if user_input == "0":
            
            # Ask user for interval to repeat function main() at
            interval = int(input("How often do you want to check for new prices?\n"))
            
            # Loop function main()   
            while True:
                # Execute function main()
                main()
                # Wait x seconds until executing function main()
                time.sleep(interval)

        # Option 2: Add pairings
        elif user_input == "1":
            while True:
                # Ask user for symbol pairings
                save_user_symbols("symbols.txt", list(input('Enter symbol pairings seperated by spaces (example: "XRPETH ETHBTC")\n').split(" ")))
                break