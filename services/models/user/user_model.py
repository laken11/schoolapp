from dataclasses import dataclass
from uuid import UUID

from services.models.base_response import BaseResponse


@dataclass
class CreateUserRequestModel:
    email: str
    role: str
    password: str
    confirm_password: str

@dataclass
class CreateUserResponseModel(BaseResponse):
    id: UUID
    email: str

@dataclass
class ForgetPasswordRequestModel:
    email: str
    password: str
    confirm_password: str
    updated_by: str

@dataclass
class ChangePasswordRequestModel:
    email: str
    current_password: str
    new_password: str
    new_confirm_password: str
    updated_by: str

@dataclass
class LoginRequestModel:
    email: str
    password: str

@dataclass
class LoginResponseModel(BaseResponse):
    id: UUID
    email: str
    role: str

@dataclass
class GetUserResponseModel(BaseResponse):
    id: UUID
    email: str
    role: str