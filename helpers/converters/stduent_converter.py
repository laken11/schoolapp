from entities.student import Student
from entities.user import User
from repositories.dto.student_dto import StudentDTO


class StudentConverter:
    @staticmethod
    def convert_entity_to_dto(entity: Student) -> StudentDTO:
        return StudentDTO(
            id=entity.id,
            user_id=entity.user_id,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
            date_created=entity.date_created,
            date_updated=entity.date_updated,
            name=entity.name,
            phone_number=entity.phone_number,
            matric_number=entity.matric_number
        )

    @staticmethod
    def convert_dto_to_entity(dto: StudentDTO) -> Student:
        return Student(created_by=dto.created_by,name=dto.name, phone_number=dto.phone_number, user_id=dto.user_id,user=dto.user)
