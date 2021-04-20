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
        "AAVEUSDT",
        "VETUSDT"
    ]
    # portfolio.write_trade_history(symbols)
    # portfolio.write_portfolio_stats("spot_order_history_1618930550877")
    # portfolio.write_porfolio_summary("portfolio_stats")
    portfolio.write_spot_balance()
