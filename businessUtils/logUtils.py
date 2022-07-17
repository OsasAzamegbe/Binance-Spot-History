from datetime import datetime
from inspect import getframeinfo, stack

class LogLevel:
    ERROR: str = "ERROR"
    INFO: str = "INFO"
    TRACE: str = "TRACE"


def log(log_level: LogLevel, *args):
    log_dir: str = "logs"
    caller = getframeinfo(stack()[1][0])
    datetime_object = datetime.now()
    log_file_name = f"{log_dir}/crypto_log{datetime_object.isoformat(timespec='hours')}.txt"
    with open(log_file_name, "a") as log_file:
        print(f"{datetime_object} - {log_level} {caller.filename}:{caller.lineno} - ", *args, file=log_file)
 