import uuid
from typing import Union, Optional

from entities.entity import Entity
from entities.user import User


class Student(Entity):
    def __init__(self, created_by: Optional[str], name: str,
                 phone_number: str, user_id: uuid.UUID, user: Optional[User] = None, matric_number: Optional[str] = None) -> None:
        super().__init__(created_by)
        self.name = name
        self.phone_number = phone_number
        self.user_id = user_id
        self.user = user
        self.matric_number = Student.__generate_matric_number() if matric_number is None else matric_number

    @staticmethod
    def __generate_matric_number() -> str:
        return str(uuid.uuid4()).split("-")[0].upper()

    def __str__(self):
        return f"Name: {self.name}\nPhone number: {self.phone_number}\nEmail: {self.user.email}\nMatric number: {self.matric_number}"