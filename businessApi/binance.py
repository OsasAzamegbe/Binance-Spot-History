from dotenv import load_dotenv
import os
import requests
from typing import Dict, List, Union, Any

from businessUtils.apiUtils import (
    compute_signature, 
    timestamp
)

load_dotenv()


BASE_URL = "https://api3.binance.com"

def _headers() -> Dict[str, str]:
    '''
    get request headers
    '''
    return {
        "X-MBX-APIKEY": os.environ['API_KEY']
    }


def _resolve_params(params: Dict[str, Any]={}) -> Dict[str, Any]:
    '''
    get request params resolved
    ''' 
    params["timestamp"] = timestamp()
    params["signature"] = compute_signature(params, os.environ["SECRET_KEY"])

    return params


def get_all_orders(symbol: str) -> Union[List, Dict]:
    '''
    get all spot trading orders.
    '''
    GET_ORDERS_ENDPOINT = f"{BASE_URL}/api/v3/allOrders"

    headers = _headers()
    params = _resolve_params({"symbol": symbol})

    response = requests.get(GET_ORDERS_ENDPOINT, params=params, headers=headers)
    return response.json()


def get_spot_account_snapshot() -> Dict[str, Any]:
    '''
    get snapshot of spot account as a Dict.
    '''
    GET_ACCOUNT_SNAPSHOT_ENDPOINT = f"{BASE_URL}/sapi/v1/accountSnapshot"

    headers = _headers()
    params = _resolve_params({"type": "SPOT"})

    response = requests.get(GET_ACCOUNT_SNAPSHOT_ENDPOINT, params=params, headers=headers)
    return response.json()


def get_ticker_price(ticker: str) -> Union[List, Dict]:
    '''
    get the latest price of a ticker.
    ''' 
    GET_TICKER_PRICE_ENDPOINT = f"{BASE_URL}/api/v3/ticker/price"

    headers = _headers()
    params = {"symbol": ticker}

    response = requests.get(GET_TICKER_PRICE_ENDPOINT, params=params, headers=headers)
    return response.json()