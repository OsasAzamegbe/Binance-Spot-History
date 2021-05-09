from typing import Dict, List, Union, Any, Set
from datetime import datetime
import time

from businessUtils.fileIOUtils import read_from_json


def _map_timestamp_to_datetime(trade_object: Dict[str, Any]) -> Dict[str, Any]:
    '''
    change the time field in trade_object from a timestamp in milliseconds to a date and time
    '''
    for timefield in ("time", "updateTime"):
        trade_object[timefield] = time.ctime(trade_object[timefield]/1000)

    return trade_object


def format_trade_history(trade_history: List[Dict[str, Any]]) -> None:
    '''
    Convert timestamps to datetime object and sort trade_history object list
    '''
    trade_history.sort(key=lambda x: x["time"])
    list(map(_map_timestamp_to_datetime, trade_history))


def reduce_field(trade_list: List[Dict[str, Any]], field: str) -> float:
    '''
    reduce (sum up) fields present in list of dict
    '''
    return sum(float(trade[field]) if trade["side"] == "BUY" else -float(trade[field]) for trade in trade_list)


def resolve_spot_trade(spot_trade: Dict[str, Any]) -> Dict[str, Any]:
    '''
    resolve fields  for a buy or sell side spot trade.
    '''
    fee_rate = 0.001

    if spot_trade["side"] == "BUY":
        spot_trade["actualQty"] = float(spot_trade["executedQty"]) * (1 - fee_rate)             # actual amount added to wallet
        spot_trade["fee"] = float(spot_trade["executedQty"]) * fee_rate                         #0.1% fee of coin quantity for buying
        spot_trade["actualCost"] = float(spot_trade["cummulativeQuoteQty"])                     #usdt
    elif spot_trade["side"] == "SELL":
        spot_trade["actualQty"] = float(spot_trade["executedQty"])
        spot_trade["fee"] = float(spot_trade["cummulativeQuoteQty"]) * fee_rate                 #0.1% fee of usdt for selling
        spot_trade["actualCost"] = float(spot_trade["cummulativeQuoteQty"]) * (1 - fee_rate)               
    else:
        raise Exception("Unknown trade side. Neither 'BUY' nor 'SELL'.")

    spot_trade["totalCost"] = float(spot_trade["cummulativeQuoteQty"])                          #usdt

    return spot_trade


def create_ticker_summary(ticker: str, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    '''
    create a ticker summary from a ticker and list of trades.
    '''       
    ticker_summary = {
        "symbol": ticker,
        "date": str(datetime.now()),
        "actualQty": reduce_field(trades, "actualQty"),
        "totalCost": reduce_field(trades, "totalCost"),
        "actualCost": reduce_field(trades, "actualCost")
    }

    return ticker_summary


def resolve_spot_balance(spot_balance: List[Dict[str, Any]], ticker_prices: Dict[str, Dict[str, str]]) -> List[Dict[str, Any]]:
    '''
    resolve spot coin balances with their prices
    '''
    return [
        {
            "symbol": balance["asset"],
            "balanceQty": balance["free"],
            "price": float(ticker_prices[balance["asset"]]["price"]),
            "actualValue": float(ticker_prices[balance["asset"]]["price"]) * float(balance["free"]),
            "locked": balance["locked"]
        }
        if balance["asset"] != "USDT" else
        {
            "symbol": balance["asset"],
            "balanceQty": balance["free"],
            "price": 1.00,
            "actualValue": float(balance["free"]),
            "locked": balance["locked"]
        }
        for balance in spot_balance
    ]


def reduce_trade_history(trade_history: List[Dict[str, Any]], new_trade_history: List[Dict[str, Any]]) -> None:
    '''
    reduce the new trade history objects into the new trade history without duplicates
    '''
    cached_trade_history: Set[int] = set(trade["orderId"] for trade in trade_history)
    trade_history.extend(trade for trade in new_trade_history if trade["orderId"] not in cached_trade_history)


def resolve_portfolio_summary(portfolio_summary: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    '''
    resolve the objects in portfolio summary
    filter objects with balance < 1 USDT and sort by most profitable.
    '''    
    spot_balance = {balance["symbol"]: balance for balance in read_from_json("spot_balance")}
    portfolio_summary = [
        {
            **summary, 
            **spot_balance[summary["symbol"].split("USDT")[0]]
        }
        for summary in portfolio_summary
    ]
    return sorted((
        {
            **summary,
            "pnlPercentage": (float(summary["actualValue"]) - float(summary["actualCost"]))/float(summary["actualCost"]) * 100
        }
        for summary in portfolio_summary
        if float(summary["actualValue"]) >= 1.0
    )
    , key=lambda x: x["pnlPercentage"], reverse=True)