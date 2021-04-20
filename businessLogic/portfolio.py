from typing import List, Dict, Any
from collections import defaultdict
import time

from businessApi.binance import (
    get_all_orders, 
    get_spot_account_snapshot
)
from businessUtils.portfolioUtils import (
    format_trade_history, 
    create_ticker_summary, 
    resolve_spot_trade
)
from businessUtils.fileIOUtils import (
    write_to_excel,
    write_to_json,
    read_from_json
)

def write_trade_history(symbols: List[str]) -> None:
    '''
    write the trade history of symbol pairs to a json file and excel file
    '''
    trade_history: List[Dict[str, Any]] = []
    for symbol in symbols:
        symbol_order_history = get_all_orders(symbol)
        trade_history.extend(symbol_order_history)

    format_trade_history(trade_history)

    filename = 'spot_order_history'
    write_to_json(trade_history, filename)
    write_to_excel(trade_history, filename)

def write_portfolio_stats(trade_history_filename:str) -> None:
    '''
    write portfolio statistics to a json file
    '''
    trade_history_dict: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for spot_trade in read_from_json(trade_history_filename):
        if spot_trade["status"] == "FILLED":                             
            trade_history_dict[spot_trade["symbol"]].append(resolve_spot_trade(spot_trade))

    write_to_json(trade_history_dict, "portfolio_stats", replace_existing=True)


def write_porfolio_summary(portfolio_stats_filename: str) -> None:
    '''
    write portfolio summary to a json file and an excel file
    '''
    porfolio_summary = []
    portfolio_stats = read_from_json(portfolio_stats_filename)

    for ticker, trades in portfolio_stats.items():
        ticker_summary = create_ticker_summary(ticker, trades)
        porfolio_summary.append(ticker_summary)

    write_to_json(porfolio_summary, "portfolio_summary", replace_existing=True)
    write_to_excel(porfolio_summary, "portfolio_summary", replace_existing=True)


def write_spot_balance() -> None:
    '''
    write latest daily snapshots of spot account to json and excel
    '''
    spot_balance = get_spot_account_snapshot()

    write_to_json(spot_balance, "spot_balance", replace_existing=True)

    latest_spot_balance = spot_balance["snapshotVos"][-1]
    balance_datetime = latest_spot_balance["updateTime"]/1000
    formatted_balance_datetime = time.strftime("%A-%d-%m-%Y_%H-%M-%S", time.localtime(balance_datetime))
    excel_filename = f"spot_balance_{formatted_balance_datetime}"

    write_to_excel(latest_spot_balance["data"]["balances"], excel_filename, replace_existing=True)
