from handlers.user_handler import UserHandler
from menu.admin_menu import AdminMenu
from menu.main_menu import MainMenu
from repositories.context import Context, MySqlDbContext
from repositories.user_repository import UserRepository
from services.continer_service import ContainerService
from services.user_service import UserService

def add_repos(container: ContainerService):
    context = container.get("context")
    user_repository = UserRepository(context)
    container.set("user_repository", user_repository)

def add_services(container: ContainerService):
    user_repository = container.get("user_repository")
    user_service = UserService(user_repository)
    container.set("user_service", user_service)

def add_handlers(container: ContainerService):
    user_service = container.get("user_service")
    user_handler = UserHandler(user_service)
    container.set("user_handler", user_handler)

def add_menus(container: ContainerService):
    container.set("main_menu", MainMenu())
    container.set("admin_menu", AdminMenu())


def set_up(container: ContainerService):
    context: Context = MySqlDbContext("localhost", "schoolApp", "root", "6h8^HP")
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
