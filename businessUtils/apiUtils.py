from businessUtils.errorUtils import ClientException
from businessUtils.logUtils import LogLevel, log

from typing import Dict, Union, Any 
from functools import wraps
import hashlib
import hmac
import time


def format_query_params(query_params: Dict[str, Union[int, str, bool]]) -> str:
    '''
    format query params from a dictionary to query string format (key1=value1&key2=value2...)
    '''
    return "".join(f"&{key}={value}" for key, value in query_params.items())[1:]


def compute_signature(query_params: Dict[str, Union[int, str, bool]], secret_key: str) -> str:
    '''
    compute a HMAC SHA256 signature with secret key as the key and the query params as the value.
    '''
    value = format_query_params(query_params)
    signature = hmac.new(bytes(secret_key, 'latin-1'), msg=bytes(value, 'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
    
    return signature

def timestamp() -> int:
    '''
    return current timestamp in milliseconds.
    '''
    return int(time.time() * 1000)

def http_request(request_function) -> Any:
    ''' base internal method for sending HTTP requests'''
    @wraps(request_function)
    def func(*args, **kwargs):
        try:
            return request_function(*args, **kwargs)
        except Exception as e:
            log(LogLevel.ERROR, str(e))
            raise ClientException(str(e))

    return func
