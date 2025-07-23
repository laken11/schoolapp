import datetime
import uuid
from enum_.role import Role
from sqlalchemy import DateTime, ForeignKey, String, CHAR, UUID, Enum, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from uuid import UUID

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __tablename__: str = None  
    
    id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True)
    date_created: Mapped[str] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC))
    date_updated: Mapped[str] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[str] = mapped_column(String(20), nullable=True)
    updated_by: Mapped[str] = mapped_column(String(20), nullable=True)
    
class User(BaseModel):
    __tablename__ = 'users'
    
    role: Mapped[str] = mapped_column(Enum(Role), default=Role.GUEST)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(500), nullable=False)
    hash_salt: Mapped[str] = mapped_column(String(500), nullable=False)
    student = relationship("Student", back_populates="user", uselist=False)
        
    
    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"

class Student(BaseModel):
    
    def __generate_matric_number__():
        return str(uuid.uuid4()).split("-")[0].upper()
    
    __tablename__ = 'students'
    
    matric_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, default=__generate_matric_number__())
    name: Mapped[str] = mapped_column(String(500), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)
    user: Mapped["User"] = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")
    
    def __repr__(self):
        return f"<Student(user_id={self.user_id}, name={self.name}, matric_number={self.matric_number})>"
    
    
class Course(BaseModel):
    __tablename__ = "courses"
    title: Mapped[str] = mapped_column(String(50),nullable=False, index=True, unique=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, index=True, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    enrollments = relationship("Enrollment", back_populates="course")
    
    def __repr__(self):
        return f"<Course(name={self.name}, code={self.code})>"
        
        
class Enrollment(BaseModel):
    __tablename__ = "enrollments"
    
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), nullable=False)
    student: Mapped["Student"] = relationship("Student", back_populates="enrollments")
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments")
    course_id: Mapped[UUID] = mapped_column(ForeignKey('courses.id'), nullable=False)
    date_enrolled: Mapped[str] = mapped_column(DateTime, nullable=False, default='CURRENT_TIMESTAMP')
    session_semester: Mapped[str] = mapped_column(String(20), nullable=False)
    assessments = relationship("Assessment", back_populates="enrollment")
    
    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, session_semester={self.session_semester})>"
    

class Assessment(BaseModel):
    __tablename__ = "assessments"
    
    score: Mapped[float]= mapped_column(DECIMAL(5, 2), nullable=False)
    grade: Mapped[str] = mapped_column(String(2), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    enrollment_id: Mapped[UUID] = mapped_column(ForeignKey('enrollments.id'), nullable=False)
    enrollment: Mapped["Enrollment"] = relationship("Enrollment", back_populates="assessments")
    
    def __repr__(self):
        return f"<Assessment(enrollment_id={self.enrollment_id}, score={self.score}, grade={self.grade}, type={self.type})>"
        