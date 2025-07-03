import re
from typing import Union, Optional


class BaseHandler:

    @staticmethod
    def validate_input(user_input: str, data_type: Optional[str] = None, regex_pat: Optional[str] = None) -> Union[
        int, str]:
        is_valid: bool = False
        while not is_valid:
            match data_type:
                case 'int':
                    try:
                        user_input = int(user_input)
                        is_valid = True
                    except ValueError:
                        is_valid = False
                case 'str':
                    try:
                        user_input = str(user_input)
                        is_valid = True
                    except ValueError:
                        is_valid = False
            if regex_pat is not None:
                is_valid = re.match(regex_pat, user_input) is not None
            if not is_valid:
                user_input = BaseHandler.__try_again()
        return user_input

    @staticmethod
    def __try_again() -> object:
        return input("Invalid input, try again: ")
