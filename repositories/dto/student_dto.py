from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from entities.user import User
from repositories.dto.user_dto import UserDto


@dataclass
class StudentDTO:
    id: UUID
    created_by: str
    updated_by: str
    date_created: datetime
    date_updated: datetime
    name: str
    phone_number: str
    matric_number: str
    user_id: UUID
    user: Optional[UserDto] = None

@dataclass
class UpdatedStudentDTO:
    name: str
    phone_number: str
    updated_by: str
    date_updated: datetime