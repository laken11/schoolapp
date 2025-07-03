from typing import Union

from handlers.base_handler import BaseHandler
from services.models.base_response import BaseResponse
from services.continer_service import ContainerService
from services.models.user.user_model import CreateUserRequestModel, LoginResponseModel, LoginRequestModel, \
    ChangePasswordRequestModel, GetUserResponseModel, ForgetPasswordRequestModel
from services.user_service import UserService


class UserHandler(BaseHandler):
    _user_service: UserService
    _container_service: ContainerService

    def __init__(self, user_service: UserService, container_service: ContainerService):
        self._user_service = user_service
        self._container_service = container_service

    def create(self, role: str) -> None:
        role = role.lower()
        email: str = self.validate_input(input("Enter email: "), "str", r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
        password: str = self.validate_input(input("Enter password: "), "str", r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        confirm_password: str = self.validate_input(input("Confirm password: "), "str",
                                                    r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        request: CreateUserRequestModel = CreateUserRequestModel(email=email, password=password,
                                                                 confirm_password=confirm_password, role=role)
        response: Union[BaseResponse, CreateUserRequestModel] = self._user_service.create(request)
        if not response.status:
            print(f"Unable to process your request: {response.message}")
        else:
            print(f"User with email {response.email} created successfully")

    def login(self) -> None:
        email = self.validate_input(input("Enter email: "), "str", r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
        password = self.validate_input(input("Enter password: "), "str")
        request: LoginRequestModel = LoginRequestModel(email=email, password=password)
        response: Union[BaseResponse, LoginResponseModel] = self._user_service.login(request)
        if not response.status:
            print(f"Unable to process your request: {response.message}")
        else:
            ## get user and store in the container
            user_response = self._user_service.get(response.email)
            if not user_response.status:
                print(f"Unable to process your request: {response.message}")
            self._container_service.set("current_user", user_response)

    def logout(self) -> None:
        self._container_service.delete("current_user")

    def change_password(self) -> None:
        current_user: GetUserResponseModel = self._container_service.get("current_user")
        if current_user is None:
            print("No current logged in user, Please kindly login!")
            return
        current_password: str = self.validate_input(input("Enter current password: "), "str",
                                                    r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        password: str = self.validate_input(input("Enter new password: "), "str",
                                            r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        confirm_password: str = self.validate_input(input("Confirm new password: "), "str",
                                                    r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        request: ChangePasswordRequestModel = ChangePasswordRequestModel(email=current_user.email,
                                                                         current_password=current_password,
                                                                         new_password=password,
                                                                         new_confirm_password=confirm_password,
                                                                         updated_by=current_user.email)
        response: BaseResponse = self._user_service.change_password(request)
        if not response.status:
            print(f"Unable to process your request: {response.message}")
        print(f"Password changed successfully")

    def forgot_password(self) -> None:
        email: str = self.validate_input(input("Enter your email: "), "str", r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        password: str = self.validate_input(input("Enter password: "), "str", r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        confirm_password: str = self.validate_input(input("Confirm password: "), "str",
                                                    r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        request: ForgetPasswordRequestModel = ForgetPasswordRequestModel(email=email, password=password,
                                                                         confirm_password=confirm_password,
                                                                         updated_by=email)
        response: BaseResponse = self._user_service.forget_password(request)
        if not response.status:
            print(f"Unable to process your request: {response.message}")
        print(f"Password changed successfully")
