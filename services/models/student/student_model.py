from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from entities.student import Student
from services.models.base_response import BaseResponse


@dataclass
class CreateStudentRequestModel:
    email: str
    name: str
    phone_number: str

@dataclass
class CreateStudentResponseModel(BaseResponse):
    email: str
    user_id: UUID
    name: str
    matric_number: str
    phone_number: str

@dataclass
class UpdateStudentRequestModel:
    name: str
    phone_number: str
    date_updated: datetime

@dataclass
class GetStudentResponseModel(BaseResponse):
    student: Student

@dataclass
class ListStudentResponseModel(BaseResponse):
    students: List[Student]