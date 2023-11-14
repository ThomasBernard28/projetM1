import os
import xlsxLoader as xlx
import xlsLoader as xl
import pandas as pd
from tempfile import NamedTemporaryFile


class Workspace:

    def __init__(self, st_uploaded_buffer, is_xls):
        """
        We take for the construction a buffer containing a that has been uploaded with
        Streamlit's file uploader and a boolean that specifies if the file
        is an .xls or .xlsx
        """

        if is_xls:
            with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
                file.write(st_uploaded_buffer)
                self.workbook = xl.parse_file(file.name)
            os.remove(file.name)

        else:
            with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
                file.write(st_uploaded_buffer)
                self.workbook = xlx.parse_file(file.name)
            os.remove(file.name)

        if self.workbook is not None:
            self.categories = self.find_all_categories()

            self.dataframes = {}
            for sheet_name in self.workbook.sheetnames:
                self.dataframes[sheet_name] = pd.DataFrame(self.workbook[sheet_name].values)

            self.students = []
            i = 4
            while i < self.workbook["Nom"].max_row:
                self.students.append(self.workbook["Nom"].cell(i, 2).value)
                i += 1

        else:
            raise TypeError("The Workbook value is None because the initialisation failed")

    def find_all_categories(self):
        categories = []
        for sheet_name in self.workbook.sheetnames:
            if sheet_name != "Nom":
                sheet = self.workbook[sheet_name]
                i = 3
                while i < sheet.max_column:
                    if sheet.cell(3, i).value in categories:
                        i += 1
                    else:
                        categories.append(sheet.cell(3, i).value)

        return categories

    def get_a_dataframe_from_sheet(self, sheet_name):
        dataframe = self.dataframes[sheet_name]
        return dataframe
