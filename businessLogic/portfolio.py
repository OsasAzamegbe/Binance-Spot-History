from typing import List

from businessApi.binance import get_all_orders
from businessUtils.portfolioUtils import format_trade_history
from businessUtils.fileIOUtils import (
    write_to_excel,
    write_to_json
)

def write_trade_history(symbols: List[str]) -> None:
    '''
    write the trade history of symbol pairs to a json file and excel file
    '''
    trade_history = []
    for symbol in symbols:
        symbol_order_history = get_all_orders(symbol)
        trade_history.extend(symbol_order_history)

    format_trade_history(trade_history)

    filename = 'spot_order_history'
    write_to_json(trade_history, filename)
    write_to_excel(trade_history, filename)