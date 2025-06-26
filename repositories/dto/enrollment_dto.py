from datetime import datetime
from typing import Optional
from uuid import UUID


class EnrollmentDTO:
    id: UUID
    created_by: str
    date_created: datetime
    date_updated: datetime
    date_enrolled: datetime
    student_id: UUID
    name: Optional[str]
    phone_number: Optional[str]
    matric_number: Optional[str]
    user_id: Optional[str]
    course_id: UUID
    code: Optional[str]
    title: Optional[str]
    description: Optional[str]