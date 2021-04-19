from businessApi import binance


if __name__ == '__main__':
    symbols = [
        "ETHUSDT",
        "BTCUSDT",
        "LINKUSDT",
        "ADAUSDT",
        "DOTUSDT",
        "SXPUSDT",
        "ENJUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "AAVEUSDT"
    ]
    binance.write_trade_history(symbols)
