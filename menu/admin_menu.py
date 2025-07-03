from handlers.user_handler import UserHandler
from menu.base_menu import BaseMenu
from menu.main_menu import MainMenu
from services.continer_service import ContainerService


class AdminMenu(BaseMenu):
    _main_menu: MainMenu
    _user_handler: UserHandler

    def __init__(self):
        self._user_handler = ContainerService.get(UserHandler.__class__.__name__)
        self._main_menu = ContainerService.get(MainMenu.__class__.__name__)

    def print_means(self):
        print(f"{self.__class__.__name__} menu started")
        print(f"{self.__class__.__name__} menu options:")
        print(f"{self.__class__.__name__} menu option 1:  User Menu\n")
        print(f"{self.__class__.__name__} menu option 2:  Student Menu\n")
        print(f"{self.__class__.__name__} menu option 3:  Logout\n")


    def handle_menu(self, option: int):
        match option:
            case 1:
                self.__print_user_menu()
                option = self.handle_user_input()
                self.__handle_user_menu(option)
            case 2:
                ...
            case 3:
                self._user_handler.logout()
                self._main_menu.print_means()
                option = self.handle_user_input()
                self._main_menu.handle_menu(option)


    def __print_user_menu(self):
        print(f"{self.__class__.__name__} menu option 1:  Create Student User\n")
        print(f"{self.__class__.__name__} menu option 2:  Create Admin User\n")
        print(f"{self.__class__.__name__} menu option 3:  Change Password\n")
        print(f"{self.__class__.__name__} menu option 4:  Forget Password\n")
        print(f"{self.__class__.__name__} menu option 5:  Go Back\n")


    def __handle_user_menu(self, option: int):
        match option:
            case 1:
                self._user_handler.create("Student")
                self.__print_user_menu()
                option = self.handle_user_input()
                self.__handle_user_menu(option)
            case 2:
                self._user_handler.create("Admin")
                self.__print_user_menu()
                option = self.handle_user_input()
                self.__handle_user_menu(option)
            case 5:
                self.print_means()
                option = self.handle_user_input()
                self.handle_menu(option)