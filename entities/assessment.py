from typing import Optional

from entities.entity import Entity


class Assessment(Entity):
    def __init__(self, created_by: Optional[str], score: float, grade: str, type: str):
        super().__init__(created_by)
        self.score = score
        self.grade = grade
        self.type = type