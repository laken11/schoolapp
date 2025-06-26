from typing import Union, Optional

from entities.entity import Entity


class Course(Entity):
    def __init__(self, created_by: Optional[str], code: str, title: str, description: str):
        super().__init__(created_by)
        self.code = code
        self.title = title
        self.description = description