import  os
from dotenv import load_dotenv
import requests
from rest_framework import status

load_dotenv()

def convert_currencies(rub_price):
    usd_price = 0
    url = os.getenv("URL")
    YOUR_API_KEY = os.getenv("YOUR_API_KEY")
    response = requests.get(
        f'{url}/{YOUR_API_KEY}/pair/RUB/USD'
    )
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()["conversion_rate"]
        usd_price = rub_price * usd_rate
    return usd_price
