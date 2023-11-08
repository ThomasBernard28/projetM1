import os
import openpyxl
from tempfile import NamedTemporaryFile
import loader


class Workspace:

    def __init__(self, st_uploaded_file):
        self.workbook = None

        if st_uploaded_file.name.endswith(".xls"):
            with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
                file.write(st_uploaded_file.getbuffer())
                self.workbook, self.students, self.class_name = loader.load_file(file.name, True)
                print(self.students)
            os.remove(file.name)

        else:
            with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
                file.write(st_uploaded_file.getbuffer())
                self.workbook, self.students, self.class_name = loader.load_file(file.name, True)
            os.remove(file.name)

    def get_student_results(self, student_name):
        return loader.get_student_results(self.workbook, student_name)
