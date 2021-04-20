from typing import Dict, List, Union, Any
import pandas as pd
import hashlib
import hmac
import time
import json


def _map_timestamp_to_datetime(trade_object: Dict[str, Any]) -> Dict[str, Any]:
    '''
    change the time field in trade_object from a timestamp in milliseconds to a date and time
    '''
    for timefield in ("time", "updateTime"):
        trade_object[timefield] = time.ctime(trade_object[timefield]/1000)

    return trade_object


def format_query_params(query_params: Dict[str, Union[int, str, bool]]) -> str:
    '''
    format query params from a dictionary to query string format (key1=value1&key2=value2...)
    '''
    return "".join(f"&{key}={value}" for key, value in query_params.items())[1:]


def compute_signature(query_params: Dict[str, Union[int, str, bool]], secret_key: str) -> str:
    '''
    compute a HMAC SHA256 signature with secret key as the key and the query params as the value.
    '''
    value = format_query_params(query_params)
    signature = hmac.new(bytes(secret_key, 'latin-1'), msg=bytes(value, 'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
    
    return signature

def timestamp() -> int:
    '''
    return current timestamp in milliseconds.
    '''
    return int(time.time() * 1000)

def write_to_json(json_object: Union[List, Dict], filename: str) -> None:
    '''
    write a json object to a json file.
    '''
    with open(f"{filename}_{str(timestamp())}.json", 'w') as file:
        json.dump(json_object, file, indent=4)


def write_to_excel(json_object: Union[List, Dict], filename: str) -> None:
    '''
    write a json object to an excel file (*.xlsx).
    '''
    pd.DataFrame(json_object).to_excel(f"{filename}_{str(timestamp())}.xlsx")


def format_trade_history(trade_history: List) -> List:
    '''
    Convert timestamps to datetime object and sort trade_history object list
    '''
    trade_history.sort(key=lambda x: x["time"])
    return list(map(_map_timestamp_to_datetime, trade_history))
