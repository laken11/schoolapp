from handlers.user_handler import UserHandler
from menu.admin_menu import AdminMenu
from menu.base_menu import BaseMenu
from services.continer_service import ContainerService


class MainMenu(BaseMenu):
    _user_handler: UserHandler
    _admin_menu: AdminMenu

    def __init__(self) -> None:
        self._user_handler = ContainerService.get(UserHandler.__class__.__name__)
        self._admin_menu = ContainerService.get(AdminMenu.__class__.__name__)

    def handle_menu(self, option: int):
        current_user = ContainerService.get("current_user")
        match option:
            case 1:
                self._user_handler.login()
                if not current_user and current_user.role is "Admin":
                    self._admin_menu.get_to_menu()
            case 0:
                SystemExit()


    def print_means(self):
        print("Welcome to the SCHOOL MANAGEMENT SYSTEM!")
        print(f"{self.__class__.__name__} menu started")
        print(f"{self.__class__.__name__} menu options:")
        print(f"{self.__class__.__name__} menu option 1:  Login\n")
        print(f"{self.__class__.__name__} menu option 0:  Exit\n")