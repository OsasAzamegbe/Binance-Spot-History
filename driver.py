from businessLogic import portfolio


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
    portfolio.write_trade_history(symbols)
