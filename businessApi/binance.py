from dotenv import load_dotenv
import os
import requests
from typing import Dict, List, Union

from businessUtils.apiUtils import (
    compute_signature, 
    timestamp
)

load_dotenv()


def get_all_orders(symbol: str) -> Union[List, Dict]:
    '''
    get all spot trading orders.
    '''
    BASE_URL = "https://api3.binance.com"
    GET_ORDERS_ENDPOINT = f"{BASE_URL}/api/v3/allOrders"

    headers = {
        "X-MBX-APIKEY": os.environ['API_KEY']
    }

    params = {
        "symbol": symbol,
        "timestamp": timestamp()
    }

    params["signature"] = compute_signature(params, os.environ["SECRET_KEY"])

    response = requests.get(GET_ORDERS_ENDPOINT, params=params, headers=headers)
    return response.json()
