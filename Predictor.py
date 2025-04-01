
import requests
import json
import pandas as pd
import time

TOKEN = "7631130153:AAGOShF-RsyxPeGwSGExu8UTUgVxtkgI_ow"
CHAT_ID = "7525050818"
API_ENDPOINT = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1h"
LIMIT = 1000

def send_telegram_message(message):
    """Send a message to Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=data)
    return response.json()

def get_telegram_updates():
    """Get updates from Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

def generate_signal():
    """Generate a buy/sell signal based on SMA"""
    params = {"symbol": SYMBOL, "interval": INTERVAL, "limit": LIMIT}
    response = requests.get(API_ENDPOINT, params=params)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    
    df["sma_50"] = df["close"].rolling(window=50).mean()
    df["sma_200"] = df["close"].rolling(window=200).mean()
    
    df["signal"] = 0
    df.loc[(df["sma_50"] > df["sma_200"]) & (df["close"] > df["sma_200"]), "signal"] = 1
    df.loc[(df["sma_50"] < df["sma_200"]) & (df["close"] < df["sma_200"]), "signal"] = -1
    
    latest_signal = df["signal"].iloc[-1]
    
    if latest_signal == 1:
        return "Buy signal: BTC/USD"
    elif latest_signal == -1:
        return "Sell signal: BTC/USD"
    else:
        return "No signal: BTC/USD"

def main():
    while True:
        signal_message = generate_signal()
        send_telegram_message(signal_message)
        time.sleep(60)  # wait for 1 minute


