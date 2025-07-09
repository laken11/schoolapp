from typing import Optional, Dict, List, Generator
from uuid import UUID

from entities.student import Student
from helpers.converters.stduent_converter import StudentConverter
from repositories.context import Context
from repositories.dto.student_dto import StudentDTO, UpdatedStudentDTO
from repositories.dto.user_dto import UserDto


class StudentRepository:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    def create(self, student: Student) -> Optional[UUID]:
        try:
            student_dto = StudentConverter.convert_entity_to_dto(student)
            query = f"""INSERT INTO students 
            (id, created_by, updated_by, date_created, date_updated, user_id, name, phone_number, matric_number) 
            VALUES (%(id)s, %(created_by)s, %(updated_by)s, %(date_created)s, %(date_updated)s, %(user_id)s, %(name)s, %(phone_number)s, %(matric_number)s)"""
            rows_affected = self._context.execute(query, student_dto)
            return student.id if rows_affected > 0 else None
        except Exception as e:
            print(e)
            return None

    def update(self, student_id: UUID, update_student_dto: UpdatedStudentDTO) -> Optional[UUID]:
        try:
            query = f"""UPDATE students SET name = %(name)s, phone_number = %(phone_number)s,
             date_updated = %(date_updated)s, updated_by = %(updated_by)s WHERE id = %(id)s"""
            rows_affected = self._context.execute(query, update_student_dto)
            return student_id if rows_affected > 0 else None
        except Exception as e:
            print(e)
            return None

    def get(self, matric_number: Optional[str] = None, student_id: Optional[UUID] = None, email: Optional[str] = None,
            user_id: Optional[UUID] = None) -> Optional[Student]:
        try:
            query = ("SELECT s.id AS student_id, s.name AS student_name, s.matric_number AS student_matric_number, "
                     "s.phone_number AS student_phone_number, s.date_created AS student_date_created, "
                     "s.created_by AS student_created_by, s.date_updated AS student_date_updated, "
                     "s.updated_by AS student_update_by, u.email AS student_user_email, u.id AS student_user_id, u.role AS student_user_role "
                     "FROM students AS s INNER JOIN users AS u ON s.user_id = u.id WHERE 1=1")
            params = {}
            if matric_number:
                query += f" AND s.matric_number = %(matric_number)s"
                params['matric_number'] = matric_number
            elif student_id:
                query += f" AND s.id = %(student_id)s"
                params['student_id'] = student_id
            elif email:
                query += f" AND u.email = %(email)s"
                params['email'] = email
            elif user_id:
                query += f" AND u.id = %(user_id)s"
                params['user_id'] = user_id
            else:
                return None
            data: Dict = self._context.get(query, params)
            student = StudentDTO(
                id=data.get('student_id'),
                name=data.get('student_name'),
                matric_number=data.get('student_matric_number'),
                phone_number=data.get('student_phone_number'),
                date_created=data.get('student_date_created'),
                date_updated=data.get('student_date_updated'),
                updated_by=data.get('student_updated_by'),
                user_id=data.get('student_user_id'),
                created_by=data.get('student_created_by'),
                user=UserDto(
                    email=data.get('student_user_email'),
                    id=data.get('student_user_id'),
                    role=data.get('student_user_role')))
            return StudentConverter.convert_dto_to_entity(student)
        except Exception as e:
            print(e)
            return None

    def list(self) -> List[Student]:
        students: List[Student] = []
        try:
            query = ("SELECT s.id AS student_id, s.name AS student_name, s.matric_number AS student_matric_numner, "
                     "s.phone_number AS student_phone_number, s.date_created AS student_date_created, "
                     "s.created_by AS student_created_by, s.date_updated AS student_date_updated, "
                     "s.updated_by AS student_update_by, u.email AS student_user_email, u.id AS student_user_id, u.role AS student_user_role "
                     "FROM students AS s INNER JOIN users AS u ON s.user_id = u.id WHERE 1=1")
            params = {}
            data: Generator[Dict, None, None] = self._context.get_many(query, params)
            for item in data:
                students.append(StudentConverter.convert_dto_to_entity(StudentDTO(
                    id=item.get('student_id'),
                    name=item.get('student_name'),
                    matric_number=item.get('student_matric_number'),
                    phone_number=item.get('student_phone_number'),
                    date_created=item.get('student_date_created'),
                    date_updated=item.get('student_date_updated'),
                    updated_by=item.get('student_updated_by'),
                    user_id=item.get('student_user_id'),
                    created_by=item.get('student_created_by'),
                    user=UserDto(
                        email=item.get('student_user_email'),
                        id=item.get('student_user_id'),
                        role=item.get('student_user_role')))))
            return students
        except Exception as e:
            print(e)
            return students
