from businessLogic import portfolio
from businessUtils.switchUtils import Switch
from businessUtils.logUtils import LogLevel, log


if __name__ == '__main__':
    try:
        symbols = (
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
            "VETUSDT",
            "MATICUSDT",
            "LTCUSDT",
            "USDTUSDT"
        )

        if Switch.check_switch("use_refactored_code"):
            pass
        else:
            portfolio.write_trade_history(symbols, replace_existing=True)
            portfolio.write_spot_balance()
            portfolio.write_portfolio_stats("spot_order_history")
            portfolio.write_portfolio_summary("portfolio_stats")
    except Exception as e:
        log(LogLevel.ERROR, str(e))
    
