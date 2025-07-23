import enum

class Role(enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    GUEST = "guest"

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]