import datetime
from python_calamine import CalamineWorkbook

import pandas as pd

def parse_file(file_path, is_xls):

    workbook = CalamineWorkbook.from_path(file_path)

    return convert_workbook_to_dataframe(workbook)

def convert_workbook_to_dataframe(workbook):
    data = []

    name_sheet = workbook.get_sheet_by_name("Nom")
    break_index_row, students = find_blank_index(name_sheet)

    for period in workbook.sheet_names:
        if period in ["Nom", "B1", "B2", "Noel", "B3", "B4", "Exam. Juin"]:
            sheet = workbook.get_sheet_by_name(period)
            break_index_col = 0

            if period == "Nom":
                break_index_col += 2

            else:
                break_index_col += find_total_or_blank_index(sheet)

            for row in range(4, break_index_row):
                student_name = students[row - 4]

                for col in range(3, break_index_col):
                    test_name = sheet.cell_value(1, col)




def find_blank_index(name_sheet):
    i = 4
    students = []
    while i < name_sheet.total_height:
        if name_sheet.cell_value(i,2) is None:
            break
        else:
            students.append(name_sheet.cell_value(i,2))
            i += 1

    return i, students

def find_total_or_blank_index(sheet):
    i = 3
    while i < sheet.total_width:
        if sheet.cell_value(1,i) == "Total SSFL" or sheet.cell_value(1, i) is None:
            break
        else:
            i += 1

    return i
