from businessApi.binance import (
    Binance,
    get_all_orders, 
    get_spot_account_snapshot,
    get_ticker_price
)
from businessApi.client import Client
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

from typing import List, Dict, Any, Set, Union
from collections import defaultdict
import time

binance = Binance()


def write_trade_history(symbols: List[str]) -> None:
    '''
    write the trade history of symbol pairs to a json file and excel file
    '''
    trade_history: List[Dict[str, Any]] = []
    for symbol in symbols:
        symbol_order_history = binance.get_all_orders(symbol)
        trade_history.extend(symbol_order_history)

    format_trade_history(trade_history)

    filename = 'spot_order_history'

    full_trade_history: List[Dict[str, Any]] = read_from_json(filename)
    reduce_trade_history(full_trade_history, trade_history)
    
    write_to_json(full_trade_history, filename)
    write_to_excel(full_trade_history, filename)

def write_portfolio_stats(trade_history_filename:str) -> None:
    '''
    write portfolio statistics to a json file
    '''
    trade_history_dict: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for spot_trade in read_from_json(trade_history_filename):
        if spot_trade["status"] == "FILLED":                             
            trade_history_dict[spot_trade["symbol"]].append(resolve_spot_trade(spot_trade))

    write_to_json(trade_history_dict, "portfolio_stats")


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

    write_to_json(portfolio_summary, "portfolio_summary")
    write_to_excel(portfolio_summary, "portfolio_summary")


def write_spot_balance() -> None:
    '''
    write latest daily snapshots of spot account to json and excel
    '''
    spot_balance_payload = binance.get_spot_account_snapshot()

    latest_spot_balance: Dict[str, Union[int, str, Dict]] = spot_balance_payload["snapshotVos"][-1]
    balance_datetime: int = latest_spot_balance["updateTime"]/1000
    if Switch.check_switch("use_new_date_format_for_balance"):
        formatted_balance_datetime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(balance_datetime))
    else:    
        formatted_balance_datetime = time.strftime("%A-%d-%m-%Y_%H-%M-%S", time.localtime(balance_datetime))
    filename = "spot_balance"
    excel_filename = f"{filename}_{formatted_balance_datetime}"

    ticker_prices = {
        balance["asset"]: binance.get_ticker_price(balance["asset"] + "USDT")
        for balance in latest_spot_balance["data"]["balances"]
        if balance["asset"] != "USDT"
    }

    spot_balance: List[Dict[str, Any]] = resolve_spot_balance(
        latest_spot_balance["data"]["balances"], 
        ticker_prices
    )

    write_to_excel(spot_balance, excel_filename)
    write_to_json(spot_balance, filename)


class Portfolio(object):
    def __init__(self):
        self.base_currency = "USDT"
        self.coins_filename = "spot_tickers"
        self.coins: Set[str] = set(read_from_json(self.coins_filename))
        self.binance: Client = Binance()

        self.spot_order_history: List[Dict[str, Any]] = []
        self.spot_trades: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.spot_balance: List[Dict[str, Any]] = []
        self.ticker_prices: Dict[str, Dict[str, str]] = defaultdict(dict)

    def update(self):
        '''
        Update the portfolio with new data from binance
        '''
        log(LogLevel.INFO, "Updating Crypto Porfolio.")
        self._write_spot_balance()
        self._write_spot_order_history()
        self._write_refined_spot_trades()

    def _write_refined_spot_trades(self) -> None:
        '''
        write refined spot trades to a json file
        '''
        log(LogLevel.INFO, "Starting refinement of spot trades.")

        for spot_trade in self.spot_order_history:
            if spot_trade["status"] == "FILLED":                             
                self.spot_trades[spot_trade["symbol"]].append(resolve_spot_trade(spot_trade))

        write_to_json(self.spot_trades, "spot_trades")
        log(LogLevel.INFO, "Successfully refined spot trades.")


    def _write_spot_order_history(self) -> None:
        '''
        write the spot trade history of symbol pairs to a json file and excel file
        '''
        log(LogLevel.INFO, "Starting spot trade order history update.")
        for symbol in self.coins:
            log(LogLevel.INFO, "Fetching spot order history for symbol: ", symbol)
            symbol_order_history = self.binance.get_all_orders(symbol + self.base_currency)
            self.spot_order_history.extend(symbol_order_history)

        format_trade_history(self.spot_order_history)

        filename = 'spot_order_history'

        log(LogLevel.INFO, "Fetching old trade order history.")
        full_trade_history: List[Dict[str, Any]] = read_from_json(filename)
        
        reduce_trade_history(full_trade_history, self.spot_order_history)
        self.spot_order_history = full_trade_history
        
        write_to_json(full_trade_history, filename)
        write_to_excel(full_trade_history, filename)
        log(LogLevel.INFO, "Success updating spot trade order history.")

    def _write_spot_balance(self) -> None:
        '''
        write latest daily snapshots of spot account to json and excel
        '''
        log(LogLevel.INFO, "Starting spot balance update.")
        spot_balance_payload = binance.get_spot_account_snapshot()
        latest_spot_balance: Dict[str, Union[int, str, Dict]] = spot_balance_payload["snapshotVos"][-1]

        self._update_tickers({
            balance["asset"] for balance in latest_spot_balance["data"]["balances"] 
            if balance["asset"] != self.base_currency
        })
        self._get_current_ticker_prices() 

        self.spot_balance: List[Dict[str, Any]] = resolve_spot_balance(
            latest_spot_balance["data"]["balances"], 
            self.ticker_prices
        )

        filename = "spot_balance"
        write_to_excel(self.spot_balance, filename)
        write_to_json(self.spot_balance, filename)
        log(LogLevel.INFO, "Success updating spot balance.")

    def _update_tickers(self, balance_tickers: Set[str]) -> None:
        '''
        update `self.coins` with new coins from the account `balance_tickers`
        '''
        self.coins |= balance_tickers
        write_to_json(list(self.coins), self.coins_filename)
        log(LogLevel.INFO, f"Updated set of coins to: {self.coins}")

    def _get_current_ticker_prices(self) -> None:
        '''
        update `self.ticker_prices` with latest price info for each tick in `tickers`
        '''
        for tick in self.coins:
            self.ticker_prices[tick] = binance.get_ticker_price(tick + self.base_currency)