from typing import Tuple, Optional, Union
from uuid import UUID

from entities.student import Student
from repositories.dto.student_dto import StudentDTO, UpdatedStudentDTO
from repositories.student_repository import StudentRepository
from services.continer_service import ContainerService
from services.models.base_response import BaseResponse
from services.models.student.student_model import CreateStudentRequestModel, UpdateStudentRequestModel, \
    CreateStudentResponseModel, GetStudentResponseModel, ListStudentResponseModel
from services.user_service import UserService


class StudentService:
    _student_repository: StudentRepository
    _user_service: UserService

    def __init__(self, student_repository: StudentRepository, user_service: UserService):
        self._student_repository = student_repository
        self._user_service = user_service

    def create(self, request: CreateStudentRequestModel) -> BaseResponse:
        user = self._user_service.get(request.email)
        if not user.status:
            return BaseResponse(message=f"User with email {request.email} not found", status=False)

        if user.role != "student":
            return BaseResponse(status=False, message="User can not be registered")

        ## check if user is already a student
        student_exists, student = self.__student_exits(request.email)
        if student_exists:
            return BaseResponse(status=False, message=f"User with email {request.email} already a student")

        current_user = ContainerService.get("current_user")
        student = Student(
            created_by=current_user.email,
            name=request.name,
            phone_number=request.phone_number,
            user_id=user.id,
        )
        student_id = self._student_repository.create(student)
        if not student_id:
            return BaseResponse(status=False, message="Unable to create student")
        return CreateStudentResponseModel(email=user.email, user_id=user.id, matric_number=student.matric_number,
                                          name=student.name, phone_number=student.phone_number, status=True,
                                          message="Created student")

    def update(self, matric_number: str, request: UpdateStudentRequestModel) -> BaseResponse:
        student = self._student_repository.get(matric_number=matric_number)
        if not student:
            return BaseResponse(message=f"Student with matric number {matric_number} not found", status=False)
        current_user = ContainerService.get("current_user")
        update_student_dto = UpdatedStudentDTO(
            id=student.id,
            updated_by=current_user.email,
            date_updated=request.date_updated,
            name=request.name,
            phone_number=request.phone_number,
        )
        student_id = self._student_repository.update(student_id=student.id, update_student_dto=update_student_dto)
        if not student_id:
            return BaseResponse(message=f"Unable to update student with ID {student_id}", status=False)
        return BaseResponse(status=True, message="Updated student")

    def get(self, student_id: Optional[UUID] = None, email: Optional[str] = None,
            matric_number: Optional[str] = None) -> Union[GetStudentResponseModel, BaseResponse]:
        student = self._student_repository.get(student_id=student_id, email=email, matric_number=matric_number)
        if not student:
            return BaseResponse(message=f"Student not found", status=False)
        return GetStudentResponseModel(student=student, status=True, message="Fetched student")

    def list(self) -> BaseResponse:
        students = self._student_repository.list()
        if not students:
            return BaseResponse(message=f"No students found", status=False)
        return ListStudentResponseModel(students=students, status=True, message="Fetched students")

    def __student_exits(self, email: str) -> Tuple[bool, Optional[Student]]:
        student = self._student_repository.get(email=email)
        if not student:
            return False, None
        return True, student
