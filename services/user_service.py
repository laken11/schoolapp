import datetime
from http.client import responses
from typing import Union, Tuple, Optional
from uuid import UUID

from entities.user import User
from helpers.converters.user_converter import UserConverter
from helpers.hashing import HashingService
from repositories.dto.user_dto import ChangePasswordDto
from repositories.user_repository import UserRepository
from services.models.base_response import BaseResponse
from services.models.user.user_model import CreateUserRequestModel, CreateUserResponseModel, ForgetPasswordRequestModel, \
    ChangePasswordRequestModel, LoginResponseModel, LoginRequestModel, GetUserResponseModel


class UserService:
    _user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create(self, request: CreateUserRequestModel) -> BaseResponse:
        ## check if user with email already exists
        user_exists, _ = self.__check_if_user_exists(request.email)
        if user_exists:
            return BaseResponse(status=False, message=f"User with email {request.email} already exists")

        ## validate password
        if request.password != request.confirm_password:
            return BaseResponse(status=False, message=f"Passwords do not match")

        ## hash_password
        hash_salt, password_hash = HashingService.hash_password(request.password)

        ## create user entity
        user = User(
            email=request.email,
            password_hash=password_hash,
            hash_salt=hash_salt,
            role=request.role,
        )
        user_id = self._user_repository.create(user)
        if not user_id:
            return BaseResponse(status=False, message=f"Unable to create user with email {request.email}")
        return CreateUserResponseModel(status=True, message=f"Created user with email {request.email}",
                                       email=request.email, id=user_id)

    def forget_password(self, request: ForgetPasswordRequestModel) -> BaseResponse:
        ## check if user with email already exists
        user_exits, user = self.__check_if_user_exists(request.email)
        if not user_exits:
            return BaseResponse(status=False, message=f"User with email {request.email} already exists")

        # validate password
        if request.password != request.confirm_password:
            return BaseResponse(status=False, message=f"Passwords do not match")
        return self.__change_password(request.password, user.email, user.id, request.updated_by)

    def change_password(self, request: ChangePasswordRequestModel) -> BaseResponse:
        ## check if user with email already exists
        user_exits, user = self.__check_if_user_exists(request.email)
        if not user_exits:
            return BaseResponse(status=False, message=f"User with email {request.email} already exists")

        # validate password
        if request.new_password != request.new_confirm_password:
            return BaseResponse(status=False, message=f"Passwords do not match")

        # validate current password
        is_current_password_valid = HashingService.validate_password(request.current_password, user.password_hash,
                                                                     user.hash_salt)
        if not is_current_password_valid:
            return BaseResponse(status=False, message=f"Current password does not match")
        return self.__change_password(password=request.new_password, email=request.email, user_id=user.id,
                                      updated_by=request.updated_by)

    def login(self, request: LoginRequestModel) -> BaseResponse:
        ## check if user with email already exists
        user_exits, user = self.__check_if_user_exists(request.email)
        if user_exits:
            return BaseResponse(status=False,
                                message=f"Unable to login with email {request.email}, email or password incorrect")

        # validate current password
        is_password_valid = HashingService.validate_password(request.password, user.password_hash, user.hash_salt)
        if not is_password_valid:
            return BaseResponse(status=False,
                                message=f"Unable to login with email {request.email}, email or password incorrect")

        return LoginResponseModel(status=True, message=f"Login successful", email=user.email, id=user.id)

    def get(self, email: Optional[str] = None, id: Optional[UUID] = None) -> BaseResponse:
        response: Optional[BaseResponse, GetUserResponseModel]
        user: Optional[User] = None
        if email:
            user = self._user_repository.get(email)
            if not user:
                return BaseResponse(status=False, message=f"User with email {email} does not exist")
        if id:
            user = self._user_repository.get(id)
            if not user:
                return BaseResponse(status=False, message=f"User with id {id} does not exist")
        if not user:
            return BaseResponse(status=False, message=f"Unable to get user with email {email} or id {id} does not exist")
        return GetUserResponseModel(status=True, message=f"Get user successful", id=user.id, email=user.email, role=user.role)

    def __change_password(self, password: str, email: str, user_id: UUID, updated_by: str) -> BaseResponse:
        hash_salt, password_hash = HashingService.hash_password(password)
        change_password_dto = ChangePasswordDto(password_hash=password_hash, hash_salt=hash_salt,
                                                updated_by=updated_by,
                                                date_updated=datetime.datetime.now(datetime.UTC))
        user_id = self._user_repository.change_password(user_id, change_password_dto)
        if not user_id:
            return BaseResponse(status=False, message=f"Unable to change password for user with email {email}")
        return BaseResponse(status=True, message=f"Changed password for user with email {email}")

    def __check_if_user_exists(self, email: str) -> Tuple[bool, Optional[User]]:
        user = self._user_repository.get(email=email)
        if not user:
            return False, None
        return True, user
