import os
import time
import requests
import subprocess
from datetime import datetime

# AYARLAR
INTERVAL = 3600  # 1 saat (saniye cinsinden)
ROOM = "lobby"

def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        response = requests.get(url).json()
        btc = response['bitcoin']['usd']
        eth = response['ethereum']['usd']
        return btc, eth
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None, None

def send_to_technocore(message):
    print(f"[{datetime.now()}] Sending: {message}")
    # Mevcut technocore_agent.py scriptini kullanarak mesajı gönderiyoruz
    cmd = ["python3", "technocore_agent.py", "say", ROOM, message]
    subprocess.run(cmd)

def main():
    print("Market Oracle Bot started! Fetching BTC and ETH prices...")
    
    while True:
        btc, eth = get_prices()
        
        if btc and eth:
            msg = f"Market Oracle: BTC is at ${btc:,} | ETH is at ${eth:,}. [Data by CoinGecko] #AgentActivity"
            send_to_technocore(msg)
        
        print(f"Waiting {INTERVAL} seconds for the next update...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
