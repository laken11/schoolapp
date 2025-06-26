from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class StudentDTO:
    id: UUID
    created_by: str
    date_created: datetime
    date_updated: datetime
    name: str
    phone_number: str
    matric_number: str
    user_id: UUID
    password_hash: Optional[str]
    hash_salt: Optional[str]
    email: Optional[str]