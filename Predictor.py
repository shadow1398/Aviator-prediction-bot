
import requests
import json
import pandas as pd
import time

Telegram bot token
TOKEN = "7631130153:AAGOShF-RsyxPeGwSGExu8UTUgVxtkgI_ow"

Telegram chat ID
CHAT_ID = "7525050818"

Define a function to send messages to Telegram
def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=data)
    return response.json()

Define a function to get updates from Telegram
def get_updates():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

Define a function to generate signals
def generate_signal():
    # Define the API endpoint for the cryptocurrency data
    api_endpoint = "https://api.binance.com/api/v3/klines"

    # Define the parameters for the API request
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 1000
    }

    # Make the API request and get the response
    response = requests.get(api_endpoint, params=params)

    # Parse the response as JSON
    data = json.loads(response.text)

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Calculate the Simple Moving Averages (SMAs)
    df["sma_50"] = df["close"].rolling(window=50).mean()
    df["sma_200"] = df["close"].rolling(window=200).mean()

    # Generate the buy and sell signals
    df["signal"] = 0
    df.loc[(df["sma_50"] > df["sma_200"]) & (df["close"] > df["sma_200"]), "signal"] = 1
    df.loc[(df["sma_50"] < df["sma_200"]) & (df["close"] < df["sma_200"]), "signal"] = -1

    # Get the latest signal
    latest_signal = df["signal"].iloc[-1]

    # Return the signal message
    if latest_signal == 1:
        return "Buy signal: BTC/USD"
    elif latest_signal == -1:
        return "Sell signal: BTC/USD"
    else:
        return "No signal: BTC/USD"

Main loop
while True:
    # Generate the signal
    signal_message = generate_signal()

    # Send the signal to Telegram
    send_message(signal_message)

    # Wait for 1 minute before generating the next signal
    time.sleep(60_seconds)
