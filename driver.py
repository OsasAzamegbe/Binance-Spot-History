from businessLogic import portfolio
from businessUtils.switchUtils import Switch
from businessUtils.logUtils import LogLevel, log
from businessLogic.portfolio import Portfolio


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
            "LTCUSDT"
        )

        if Switch.check_switch("use_refactored_code"):
            Portfolio(symbols)
        else:
            log(LogLevel.INFO, "Starting driver")
            portfolio.write_trade_history(symbols)
            portfolio.write_spot_balance()
            portfolio.write_portfolio_stats("spot_order_history")
            portfolio.write_portfolio_summary("portfolio_stats")
    except Exception as e:
        log(LogLevel.ERROR, str(e))
        raise e
    
