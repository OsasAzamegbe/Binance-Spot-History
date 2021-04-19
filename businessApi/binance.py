from dotenv import load_dotenv
import os
import requests
from typing import Dict, List, Union

from businessUtils.apiUtils import compute_signature, timestamp, write_to_json, write_to_excel

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


def write_trade_history(symbols: List[str]) -> None:
    '''
    write the trade history of symbol pairs to a json file and excel file
    '''
    trade_history = []
    for symbol in symbols:
        symbol_order_history = get_all_orders(symbol)
        trade_history.extend(symbol_order_history)

    #sort trades from oldest to newest
    trade_history.sort(key=lambda x: x["time"])

    write_to_json(trade_history, 'spot_order_history')
    write_to_excel(trade_history, 'spot_order_history')
