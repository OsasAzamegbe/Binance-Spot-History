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
    portfolio.write_trade_history(symbols, replace_existing=True)
    portfolio.write_portfolio_stats("spot_order_history")
    portfolio.write_spot_balance()
    portfolio.write_portfolio_summary("portfolio_stats")
