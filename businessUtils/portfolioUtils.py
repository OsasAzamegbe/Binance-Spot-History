from typing import Dict, List, Union, Any
import time


def _map_timestamp_to_datetime(trade_object: Dict[str, Any]) -> Dict[str, Any]:
    '''
    change the time field in trade_object from a timestamp in milliseconds to a date and time
    '''
    for timefield in ("time", "updateTime"):
        trade_object[timefield] = time.ctime(trade_object[timefield]/1000)

    return trade_object


def format_trade_history(trade_history: List) -> None:
    '''
    Convert timestamps to datetime object and sort trade_history object list
    '''
    trade_history.sort(key=lambda x: x["time"])
    list(map(_map_timestamp_to_datetime, trade_history))