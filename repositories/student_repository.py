from typing import Optional, Dict, List, Generator
from uuid import UUID

from repositories.context import Context
from repositories.dto.student_dto import StudentDTO, UpdatedStudentDTO


class StudentRepository:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    def create(self, student: StudentDTO) -> Optional[UUID]:
        try:
            query = f"""INSERT INTO students 
            (id, created_by, updated_by, date_created, date_updated, user_id, name, phone_number, matric_number) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            student_id = self._context.execute(query, student)
            return UUID(str(student_id))
        except Exception as e:
            print(e)
            return None

    def update(self, student_id: UUID, update_student_dto: UpdatedStudentDTO) -> Optional[UUID]:
        try:
            query = f"""UPDATE students SET name = %(name)s, phone_number = %(phone_number)s,
             date_updated = %(date_updated)s, updated_by = %(updated_by)s WHERE id = %(id)s"""
            params = {
                'id': student_id,
                'updated_by': update_student_dto.updated_by,
                'date_updated': update_student_dto.date_updated,
                'name': update_student_dto.name,
                'phone_number': update_student_dto.phone_number,

            }
            student_id = self._context.execute(query, params)
            return UUID(str(student_id))
        except Exception as e:
            print(e)
            return None

    def get(self, matric_number: Optional[str] = None, student_id: Optional[UUID] = None, email: Optional[str] = None,
            user_id: Optional[UUID] =None) -> Optional[StudentDTO]:
       try:
           query = ("SELECT s.id AS student_id, s.name AS student_name, s.matric_number AS student_matric_numner, "
                    "s.phone_number AS student_phone_number, s.date_created AS student_date_created, "
                    "s.created_by AS student_created_by, s.date_updated AS student_date_updated, "
                    "s.updated_by AS student_update_by, u.email AS stduent_email, u.id stduent_user_id  "
                    "FROM students AS s INNER JOIN users AS u ON s.id = u.id WHERE 1=1")
           params = {}
           if matric_number:
               query += f" AND s.matric_number = '{matric_number}'"
               params['matric_number'] = matric_number
           elif student_id:
               query += f" AND s.id = {student_id}"
               params['student_id'] = student_id
           elif email:
               query += f" AND u.email = {email}"
               params['email'] = email
           elif user_id:
               query += f" AND u.id = {user_id}"
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
               email=data.get('student_email'),
               created_by=data.get('student_created_by')
           )
           return student
       except Exception as e:
           print(e)
           return None

    def list(self) -> List[StudentDTO]:
        students: List[StudentDTO] = []
        try:
            query = ("SELECT s.id AS student_id, s.name AS student_name, s.matric_number AS student_matric_numner, "
                     "s.phone_number AS student_phone_number, s.date_created AS student_date_created, "
                     "s.created_by AS student_created_by, s.date_updated AS student_date_updated, "
                     "s.updated_by AS student_update_by, u.email AS stduent_email, u.id stduent_user_id  "
                     "FROM students AS s INNER JOIN users AS u ON s.id = u.id")
            params = {}
            data: Generator[Dict, None, None] = self._context.get_many(query, params)
            for item in data:
                students.append(StudentDTO(
                    id=item.get('student_id'),
                    name=item.get('student_name'),
                    matric_number=item.get('student_matric_number'),
                    phone_number=item.get('student_phone_number'),
                    date_created=item.get('student_date_created'),
                    date_updated=item.get('student_date_updated'),
                    updated_by=item.get('student_updated_by'),
                    user_id=item.get('student_user_id'),
                    email=item.get('student_email'),
                    created_by=item.get('student_created_by')
                ))
            return students
        except Exception as e:
            print(e)
            return students