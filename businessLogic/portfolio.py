from businessApi.binance import (
    Binance,
    get_all_orders, 
    get_spot_account_snapshot,
    get_ticker_price
)
from businessUtils.portfolioUtils import (
    format_trade_history, 
    create_ticker_summary, 
    resolve_spot_trade,
    reduce_trade_history,
    resolve_spot_balance,
    resolve_portfolio_summary
)
from businessUtils.fileIOUtils import (
    write_to_excel,
    write_to_json,
    read_from_json
)
from businessUtils.switchUtils import Switch
from businessUtils.logUtils import LogLevel, log

from typing import List, Dict, Any, Tuple
from collections import defaultdict
import time


def write_trade_history(symbols: List[str], replace_existing: bool = True) -> None:
    '''
    write the trade history of symbol pairs to a json file and excel file
    '''
    trade_history: List[Dict[str, Any]] = []
    for symbol in symbols:
        symbol_order_history = get_all_orders(symbol)
        trade_history.extend(symbol_order_history)

    format_trade_history(trade_history)

    filename = 'spot_order_history'

    full_trade_history: List[Dict[str, Any]] = read_from_json(filename)
    reduce_trade_history(full_trade_history, trade_history)
    
    write_to_json(full_trade_history, filename, replace_existing)
    write_to_excel(full_trade_history, filename, replace_existing)

def write_portfolio_stats(trade_history_filename:str) -> None:
    '''
    write portfolio statistics to a json file
    '''
    trade_history_dict: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for spot_trade in read_from_json(trade_history_filename):
        if spot_trade["status"] == "FILLED":                             
            trade_history_dict[spot_trade["symbol"]].append(resolve_spot_trade(spot_trade))

    write_to_json(trade_history_dict, "portfolio_stats", replace_existing=True)


def write_portfolio_summary(portfolio_stats_filename: str) -> None:
    '''
    write portfolio summary to a json file and an excel file
    '''
    portfolio_summary = []
    portfolio_stats = read_from_json(portfolio_stats_filename)

    for ticker, trades in portfolio_stats.items():
        ticker_summary = create_ticker_summary(ticker, trades)
        portfolio_summary.append(ticker_summary)

    portfolio_summary = resolve_portfolio_summary(portfolio_summary)

    write_to_json(portfolio_summary, "portfolio_summary", replace_existing=True)
    write_to_excel(portfolio_summary, "portfolio_summary", replace_existing=True)


def write_spot_balance() -> None:
    '''
    write latest daily snapshots of spot account to json and excel
    '''
    spot_balance_payload = get_spot_account_snapshot()

    latest_spot_balance = spot_balance_payload["snapshotVos"][-1]
    balance_datetime = latest_spot_balance["updateTime"]/1000
    if Switch.check_switch("use_new_date_format_for_balance"):
        formatted_balance_datetime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(balance_datetime))
    else:    
        formatted_balance_datetime = time.strftime("%A-%d-%m-%Y_%H-%M-%S", time.localtime(balance_datetime))
    filename = "spot_balance"
    excel_filename = f"{filename}_{formatted_balance_datetime}"

    ticker_prices = {
        balance["asset"]: get_ticker_price(balance["asset"] + "USDT")
        for balance in latest_spot_balance["data"]["balances"]
        if balance["asset"] != "USDT"
    }

    spot_balance: List[Dict[str, Any]] = resolve_spot_balance(
        latest_spot_balance["data"]["balances"], 
        ticker_prices
    )

    write_to_excel(spot_balance, excel_filename, replace_existing=True)
    write_to_json(spot_balance, filename, replace_existing=True)


class Portfolio(object):
    def __init__(self, trade_pairs: Tuple[str]):
        self.trade_pairs = trade_pairs
        self.binance = Binance()

    def write_trade_history(self) -> None:
        '''
        write the trade history of symbol pairs to a json file and excel file
        '''
        trade_history: List[Dict[str, Any]] = []
        for symbol in self.trade_pairs:
            log(LogLevel.INFO, "Fetching order history for symbol: ", symbol)
            symbol_order_history = self.binance.get_all_orders(symbol)
            trade_history.extend(symbol_order_history)

        format_trade_history(trade_history)

        filename = 'spot_order_history'

        log(LogLevel.INFO, "Fetching old trade order history")
        full_trade_history: List[Dict[str, Any]] = read_from_json(filename)
        reduce_trade_history(full_trade_history, trade_history)
        log(LogLevel.INFO, "Success updating trade order history: ", full_trade_history)
        
        write_to_json(full_trade_history, filename)
        write_to_excel(full_trade_history, filename)