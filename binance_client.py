from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

def create_client(api_key, api_secret):
    return Client(api_key, api_secret)

master_api = create_client(os.getenv("MASTER_API_KEY"), os.getenv("MASTER_API_SECRET"))
