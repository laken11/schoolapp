import abc


class BaseMenu(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle_menu(self, option: int):
        """Not Implemented"""

    @abc.abstractmethod
    def print_menu(self):
        """Not Implemented"""

    @classmethod
    def handle_user_input(cls) -> int:
        is_valid = False
        option = input("Enter Your Option: ")
        while not is_valid:
            try:
                option = int(option)
                is_valid = True
            except ValueError:
                is_valid = False
            if not is_valid:
                option = cls.__try_again()
        return option

    @classmethod
    def __try_again(cls) -> object:
        return input("Invalid input, try again: ")

    def get_to_menu(self):
        self.print_menu()
        option = self.handle_user_input()
        self.handle_menu(option)