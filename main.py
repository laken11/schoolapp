import os

from handlers.student_handler import StudentHandler
from handlers.user_handler import UserHandler
from menu.admin_menu import AdminMenu
from menu.main_menu import MainMenu
from repositories.context import Context, MySqlDbContext
from repositories.student_repository import StudentRepository
from repositories.user_repository import UserRepository
from services.continer_service import ContainerService
from services.student_service import StudentService
from services.user_service import UserService
from dotenv import load_dotenv

load_dotenv()

def add_repos(container: ContainerService):
    context = container.get("context")
    user_repository = UserRepository(context)
    container.set("user_repository", user_repository)
    student_repository = StudentRepository(context)
    container.set("student_repository", student_repository)

def add_services(container: ContainerService):
    user_repository = container.get("user_repository")
    user_service = UserService(user_repository)
    container.set("user_service", user_service)
    student_repository = container.get("student_repository")
    user_service = container.get("user_service")
    student_service = StudentService(student_repository, user_service)
    container.set("student_service", student_service)

def add_handlers(container: ContainerService):
    user_service = container.get("user_service")
    user_handler = UserHandler(user_service)
    container.set("user_handler", user_handler)
    student_service = container.get("student_service")
    student_handler = StudentHandler(student_service)
    container.set("student_handler", student_handler)

def add_menus(container: ContainerService):
    container.set("main_menu", MainMenu())
    container.set("admin_menu", AdminMenu())


def set_up(container: ContainerService):
    context: Context = MySqlDbContext(os.getenv("DB_HOST"), os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))
    container.set("context", context)
    add_repos(container)
    add_services(container)
    add_handlers(container)
    add_menus(container)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    container: ContainerService = ContainerService()
    set_up(container)
    main_menu: MainMenu = container.get("main_menu")
    main_menu.run()
