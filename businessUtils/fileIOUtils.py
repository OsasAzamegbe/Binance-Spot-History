from businessUtils.apiUtils import timestamp
from businessUtils.logUtils import LogLevel, log

from typing import Dict, List, Union, Any
import pandas as pd
import json


def write_to_json(json_object: Union[List, Dict], filename: str, replace_existing: bool=True) -> None:
    '''
    write a json object to a json file.
    '''
    if not replace_existing:
        filename = f"{filename}_{str(timestamp())}"

    with open(f"{filename}.json", 'w') as file:
        log(LogLevel.INFO, f"Writing to JSON file: '{filename}.json' with replace_existing={replace_existing}.")
        json.dump(json_object, file, indent=4)


def write_to_excel(json_object: Union[List, Dict], filename: str, replace_existing: bool=True) -> None:
    '''
    write a json object to an excel file (*.xlsx).
    '''
    if not replace_existing:
        filename = f"{filename}_{str(timestamp())}"

    log(LogLevel.INFO, f"Writing to EXCEL file: '{filename}.xlsx' with replace_existing={replace_existing}.")
    pd.DataFrame(json_object).to_excel(f"{filename}.xlsx")


def read_from_json(filename: str) -> Union[List, Dict]:
    '''
    reads data from a json file
    '''
    with open(f"{filename}.json", 'r') as json_file:
        log(LogLevel.INFO, f"Reading from JSON file: '{filename}.json'.")
        return json.load(json_file)

