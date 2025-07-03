from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class UserDto:
    id: UUID
    email: str
    role: str
    date_created: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    date_updated: Optional[datetime] = None
    password_hash: Optional[str] = None
    hash_salt: Optional[str] = None

@dataclass
class ChangePasswordDto:
    password_hash: str
    hash_salt: str
    updated_by: str
    date_updated: datetime
