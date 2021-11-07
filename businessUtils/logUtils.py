from datetime import datetime
from inspect import getframeinfo, stack

class LogLevel:
    ERROR: str = "ERROR"
    INFO: str = "INFO"
    TRACE: str = "TRACE"


def log(log_level: LogLevel, *args):
    caller = getframeinfo(stack()[1][0])
    print(f"{datetime.now()} - {log_level} {caller.filename}:{caller.lineno} - ", *args)
