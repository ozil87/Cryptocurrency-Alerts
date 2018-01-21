# https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay

# Chat bot to notify about cryptocurrency alerts
# Port of cryptocurrency_alerts.py to a Telegram bot

from binance_api import get_binance_time, get_binance_all_prices, get_symbol, save_to_json, read_from_json
import json, requests, time, urllib, os.path

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

TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

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

    text, chat = get_last_chat_id_and_text(get_updates())
    if text == "/notifyme":
        message_list = []
        message_list.append(f"The server time from the Binance API is currently {current_server_time}.")
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
                    message_list.append(f"The price for {symbol_name} is the same as its previous price and is currently {symbol_price}.")
                
                # Check if last_symbol_price is less than symbol_price
                elif last_symbol_name == symbol_name and last_symbol_price < symbol_price:
                    # Print last_symbol_price is less than symbol_price
                    message_list.append(f"The price for {symbol_name} is up from its previous price of {last_symbol_price} and is currently {symbol_price}.")

                # Check if last_symbol_price is greater than symbol_price
                elif last_symbol_name == symbol_name and last_symbol_price > symbol_price:
                    # Print last_symbol_price is greater than symbol_price
                    message_list.append(f"The price for {symbol_name} is down from its previous price of {last_symbol_price} and is currently {symbol_price}.")

            # If variable last_prices does not exist
            else:
                # Print symbol name and symbol price
                message_list.append(f"The price for {symbol_name} is currently {symbol_price}.")
        # Send complete message
        print(f"Sending a message at {current_server_time}.")
        send_message("\n".join(message_list), chat)

if __name__ == '__main__':
    # Set prices.txt to None
    save_to_json("prices.txt", None)
    # Create symbols.txt if it does not exist
    if os.path.isfile("symbols.txt") == False:
        with open("symbols.txt", "w+") as file:
            file.write("")
            file.close()
    while True:
        # Menu
        user_input = str(input("[0] Begin monitoring prices\n[1] View current symbol pairings\n[2] Select symbol pairings to monitor\n"))

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

        # Option 2: View pairings
        elif user_input == "1":
            while True:
                # Set variable symbols to current symbol pairings
                symbols = get_user_symbols("symbols.txt")
                if symbols:
                    print(" ".join(symbols))
                    break
                else:
                    print("There are currently no symbol pairings.")
                    break
        # Option 3: Add pairings
        elif user_input == "2":
            while True:
                # Ask user for symbol pairings
                save_user_symbols("symbols.txt", list(input('Enter symbol pairings seperated by spaces (example: "XRPETH ETHBTC")\n').split(" ")))
                break