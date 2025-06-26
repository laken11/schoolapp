import datetime
from typing import Optional

from entities.course import Course
from entities.entity import Entity
from entities.student import Student


class Enrollment(Entity):
    def __init__(self, created_by: Optional[str], course: Course,
                 student: Student, date_enrolled: datetime, session_semester: str):
        super().__init__(created_by)
        self.course = course
        self.student = student
        self.date_enrolled = date_enrolled
        self.session_semester = session_semester
