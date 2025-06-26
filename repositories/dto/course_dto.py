from dataclasses import  dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CourseDTO:
    id: UUID
    created_by: str
    updated_by: Optional[str]
    date_created: Optional[datetime]
    date_updated: Optional[datetime]
    code: str
    title: str
    description: str