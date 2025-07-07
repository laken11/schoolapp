from services.continer_service import ContainerService
from handlers import BaseHandler
from menu.base_menu import BaseMenu

class MainMenu(BaseMenu):
    _user_handler: BaseHandler

    def __init__(self):
        self._user_handler = ContainerService.get("user_handler")

    def handle_menu(self, option: int):
        match option:
            case 1:
                self._user_handler.login()
                current_user = ContainerService.get("current_user")
                if current_user and current_user.role.lower() == "Admin".lower():
                    ContainerService.get("admin_menu").get_to_menu()
                self.print_menu()
                option: int = self.handle_user_input()
                self.handle_menu(option)
            case 0:
                SystemExit()

    def print_menu(self):
        print("Welcome to the SCHOOL MANAGEMENT SYSTEM!")
        print(f"{self.__class__.__name__} menu started")
        print(f"{self.__class__.__name__} menu options:\t")
        print(f"{self.__class__.__name__} menu option 1:  Login\n")
        print(f"{self.__class__.__name__} menu option 2:  Create User\n")
        print(f"{self.__class__.__name__} menu option 0:  Exit\n")

    def run(self):
        self.print_menu()
        option: int = self.handle_user_input()
        self.handle_menu(option)