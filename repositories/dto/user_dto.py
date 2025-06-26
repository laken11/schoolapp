from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class UserDto:
    id: UUID
    email: str
    date_created: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    date_updated: Optional[datetime] = None
    password_hash: Optional[str] = None
    hash_salt: Optional[str] = None
