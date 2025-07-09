from entities.student import Student
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
            matric_number=entity.matric_number,
            user=entity.user,
        )

    @staticmethod
    def convert_dto_to_entity(dto: StudentDTO) -> Student:
        student = Student(created_by=dto.created_by,name=dto.name, phone_number=dto.phone_number, user_id=dto.user_id,user=dto.user, matric_number=dto.matric_number)
        student.id = dto.id
        student.updated_by = dto.updated_by
        student.date_created = dto.date_created
        student.date_updated = dto.date_updated
        return student
