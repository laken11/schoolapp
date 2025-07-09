from datetime import datetime, UTC

from handlers import BaseHandler
from services.models.student.student_model import CreateStudentRequestModel, UpdateStudentRequestModel
from services.student_service import StudentService


class StudentHandler(BaseHandler):
    _student_service: StudentService

    def __init__(self, student_service: StudentService):
        self._student_service = student_service

    def create(self):
        email = self.validate_input(user_input=input("Enter student email address: "), data_type="str", regex_pat=r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
        name = self.validate_input(user_input=input("Enter student name: "), data_type="str")
        phone_number = self.validate_input(user_input=input("Enter student phone number: "), data_type="str", regex_pat=r'(?:\+?(\d{1,3}))?')
        request: CreateStudentRequestModel = CreateStudentRequestModel(email=email, name=name, phone_number=phone_number)
        response = self._student_service.create(request)
        print(response.message)

    def update(self):
        matric_number = self.validate_input(user_input=input("Provider student matric number: "), data_type="str")
        name = self.validate_input(user_input=input("Enter student name: "), data_type="str")
        phone_number = self.validate_input(user_input=input("Enter student phone number: "), data_type="str",
                                           regex_pat=r'(?:\+?(\d{1,3}))?')

        request = UpdateStudentRequestModel(name=name, phone_number=phone_number, date_updated=datetime.now(UTC))
        response = self._student_service.update(matric_number=matric_number, request=request)
        print(response.message)

    def get(self):
        matric_number = self.validate_input(user_input=input("Provider student matric number: "), data_type="str")
        response = self._student_service.get(matric_number=matric_number)
        if not response.status:
            print("Student not found")
        else:
            print("Fetched student:\n")
            print(str(response.student))

    def list(self):
        response = self._student_service.list()
        if not response.status:
            print("Student not found")
        else:
            print("Fetched students:\n")
            for student in response.students:
                print(f"{str(student)}\n")
