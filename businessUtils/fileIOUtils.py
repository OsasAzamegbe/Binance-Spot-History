from typing import Dict, List, Union, Any
import pandas as pd
import json

from businessUtils.apiUtils import timestamp


def write_to_json(json_object: Union[List, Dict], filename: str) -> None:
    '''
    write a json object to a json file.
    '''
    with open(f"{filename}_{str(timestamp())}.json", 'w') as file:
        json.dump(json_object, file, indent=4)


def write_to_excel(json_object: Union[List, Dict], filename: str) -> None:
    '''
    write a json object to an excel file (*.xlsx).
    '''
    pd.DataFrame(json_object).to_excel(f"{filename}_{str(timestamp())}.xlsx")