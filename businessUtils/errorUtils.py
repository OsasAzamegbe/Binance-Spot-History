class RuntimeException(Exception):
    '''General Exception raised when problem occurs at runtime.'''
    pass

class ClientException(Exception):
    '''Client Execption raised when external errors occur with API calls.'''
    pass