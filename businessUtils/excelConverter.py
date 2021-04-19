import pandas as pd
from typing import List, Dict


def convert_csv_to_excel(csv_dirs: List[Dict[str, str]]) -> None:
    for csv in csv_dirs:
        csv_file = pd.read_csv(csv['csv_dir'])
        csv_file.to_excel(csv['des_dir'], index=None, header=True)


if __name__ == '__main__':
    CSV_DIRS = [
        {
            "csv_dir": './transactions_SharePool_Universal.csv',
            "des_dir": './transactions.xlsx'
        }
    ]

    convert_csv_to_excel(CSV_DIRS)
