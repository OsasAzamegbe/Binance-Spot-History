from typing import Dict, List, Union, Any
import pandas as pd
import json

from businessUtils.apiUtils import timestamp


def write_to_json(json_object: Union[List, Dict], filename: str, replace_existing: bool=True) -> None:
    '''
    write a json object to a json file.
    '''
    if not replace_existing:
        filename = f"{filename}_{str(timestamp())}"

    with open(f"{filename}.json", 'w') as file:
        json.dump(json_object, file, indent=4)


def write_to_excel(json_object: Union[List, Dict], filename: str, replace_existing: bool=True) -> None:
    '''
    write a json object to an excel file (*.xlsx).
    '''
    if not replace_existing:
        filename = f"{filename}_{str(timestamp())}"

    pd.DataFrame(json_object).to_excel(f"{filename}.xlsx")


def read_from_json(filename: str) -> Union[List, Dict]:
    '''
    reads data from a json file
    '''
    with open(f"{filename}.json", 'r') as json_file:
        return json.load(json_file)

