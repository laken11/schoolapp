from handlers.student_handler import StudentHandler
from menu.base_menu import BaseMenu
from services.continer_service import ContainerService
from menu.main_menu import MainMenu
from handlers import UserHandler

class AdminMenu(BaseMenu):
    _user_handler: UserHandler
    _student_handler: StudentHandler

    def __init__(self):
        self._user_handler = ContainerService.get("user_handler")
        self._student_handler = ContainerService.get("student_handler")

    def print_menu(self):
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
                ContainerService.get("main_menu").print_menu()
                option = self.handle_user_input()
                ContainerService.get("main_menu").handle_menu(option)

    def __print_student_menu(self):
        print(f"{self.__class__.__name__} menu option 1:  Create Student\n")
        print(f"{self.__class__.__name__} menu option 2:  Update Student\n")
        print(f"{self.__class__.__name__} menu option 3:  Get Student\n")
        print(f"{self.__class__.__name__} menu option 4:  List Student\n")
        print(f"{self.__class__.__name__} menu option 5:  Go Back\n")

    def __handle_student_menu(self, option: int):
        match option:
            case 1:
                self._student_handler.create()
                self.__print_student_menu()
                option = self.handle_user_input()
                self.__handle_student_menu(option)
            case 2:
                self._student_handler.update()
                self.__print_student_menu()
                option = self.handle_user_input()
                self.__handle_student_menu(option)
            case 3:
                self._student_handler.get()
                self.__print_student_menu()
                option = self.handle_user_input()
                self.__handle_student_menu(option)
            case 4:
                self._student_handler.list()
                self.__print_student_menu()
                option = self.handle_user_input()
                self.__handle_student_menu(option)
            case 5:
                self.print_menu()
                option = self.handle_user_input()
                self.handle_menu(option)

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
            case 3:
                self._user_handler.change_password()
                self.__print_user_menu()
                option = self.handle_user_input()
                self.__handle_user_menu(option)
            case 4:
                self._user_handler.forgot_password()
                self.__print_user_menu()
                option = self.handle_user_input()
                self.__handle_user_menu(option)
            case 5:
                self.print_menu()
                option = self.handle_user_input()
                self.handle_menu(option)