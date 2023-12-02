import datetime

import xlsConverter as xlc
import pandas as pd
import openpyxl


def parse_file(file_path, is_xls):
    if is_xls:
        workbook = xlc.convert_to_xlsx(file_path)

    else:
        workbook = openpyxl.load_workbook(file_path)

    return convert_workbook_to_dataframe(workbook)


def convert_workbook_to_dataframe(workbook):
    """
    This method converts a multiple worksheets openpyxl's workbook into a single structured pandas dataframe
    :param workbook: The multiple worksheets openpyxl's workbook
    :return: The structured pandas dataframe
    """
    # data = [["Jade", "B1", "Test 1", "SSFL", 20, 14], ["Julien", "B2", "Test 4", "CA", 15, 10]]
    # The data list will contain the records that will be used to create the dataframe
    data = []

    name_sheet = workbook["Nom"]
    break_index_row, students = find_blank_index(name_sheet)

    for period in workbook.sheetnames:
        if period in ["Nom", "B1", "B2", "Noel", "B3", "B4", "Exam. Juin"]:
            sheet = workbook[period]
            break_index_col = 0

            if period == "Nom":
                break_index_col += 2

            else:
                break_index_col += find_total_or_blank_index(sheet)

            for row in range(4, break_index_row):
                student_name = students[row - 4]

                for col in range(3, break_index_col):
                    test_name = sheet.cell(1, col).value
                    if isinstance(test_name, float):
                        # It means that the value is an Excel date
                        # 1/1/1900 is a standard for Excel
                        date_format = datetime.datetime(1900, 1, 1) + datetime.timedelta(days=test_name - 2)
                        test_name = date_format.strftime('%d-%m-%Y')
                    total = sheet.cell(2, col).value
                    competence = str(sheet.cell(3, col).value)
                    result = sheet.cell(row, col).value

                    record = [student_name, period, test_name, competence, total, result]
                    data.append(record)

    df = pd.DataFrame(data, columns=['Name', 'Period', 'Test', 'Competence', 'Total', 'Result'])

    return df


def find_blank_index(name_sheet):
    # The rows before this index doesn't contain names
    i = 4
    students = []
    while i < name_sheet.max_row:
        if name_sheet.cell(i, 2).value is None:
            break
        else:
            students.append(name_sheet.cell(i, 2).value)
            i += 1
    return i, students


def find_total_or_blank_index(sheet):
    i = 3
    while i < sheet.max_column:
        if sheet.cell(1, i).value == "Total SSFL" or sheet.cell(1, i).value is None:
            break
        else:
            i += 1
    return i
