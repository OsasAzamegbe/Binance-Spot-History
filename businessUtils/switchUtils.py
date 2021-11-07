from businessUtils.errorUtils import RuntimeException
from typing import Dict


class Switch:
    switches: Dict[str, bool] = {
        "use_refactored_code": False,
        "use_new_date_format_for_balance": True
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def check_switch(cls, switch_name: str) -> bool:
        try:
            return cls.switches[switch_name]
        except KeyError:
            raise RuntimeException(f"Switch: '{switch_name}' does not exist.")
