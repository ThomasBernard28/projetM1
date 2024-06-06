import datetime

import xlsConverter as xlc
import pandas as pd
import openpyxl


def get_periods(file_path, is_xls):
    if is_xls:
        periods = xlc.get_periods(file_path)
    else:
        workbook = openpyxl.load_workbook(file_path)
        periods = workbook.sheetnames

    return periods


def parse_file(file_path, is_xls, periods):
    if is_xls:
        workbook = xlc.convert_to_xlsx(file_path)

    else:
        workbook = openpyxl.load_workbook(file_path)

    return convert_workbook_to_dataframe(workbook, periods)


def convert_workbook_to_dataframe(workbook, periods):
    """
    This method converts a multiple worksheets openpyxl's workbook into a single structured pandas dataframe
    :param workbook: The multiple worksheets openpyxl's workbook
    :return: The structured pandas dataframe
    """

    # The data list will contain the records that will be used to create the dataframe
    data = []

    # In order to address the problem where two different tests have the same name
    test_name_counts = {}

    name_sheet = workbook["Nom"]
    break_index_row, students = find_blank_index(name_sheet)

    for period in workbook.sheetnames:
        if period in periods:
            sheet = workbook[period]
            test_names = update_test_name_counts(sheet, test_name_counts)
            break_index_col = 0

            if period == "Nom":
                break_index_col += 2

            else:
                break_index_col += find_max_col_index(sheet)

            for row in range(4, break_index_row):
                student_name = students[row - 4]

                for col in range(3, break_index_col):
                    # Takes the unique test name to prevent duplicates
                    test_name = test_names[col]

                    total = sheet.cell(2, col).value
                    competence = str(sheet.cell(3, col).value)
                    result = sheet.cell(row, col).value

                    record = [student_name, period, test_name, competence, total, result]
                    data.append(record)

    df = pd.DataFrame(data, columns=['Name', 'Period', 'Test', 'Competence', 'Total', 'Result'])

    return df


def update_test_name_counts(sheet, test_name_counts):
    unique_test_names = {}
    col_index = 3
    while col_index < sheet.max_column:
        test_name = get_test_name(sheet, col_index)
        if test_name not in test_name_counts:
            test_name_counts[test_name] = 1
            # First occurrence of the test keeps the original name
            unique_test_names[col_index] = test_name
        else:
            test_name_counts[test_name] += 1
            new_name = f"{test_name} - {test_name_counts[test_name]}"
            unique_test_names[col_index] = new_name
        col_index += 1
    return unique_test_names


def get_test_name(sheet, col):
    test_name = sheet.cell(1, col).value

    # If it is .xls then the date is a float
    if isinstance(test_name, float):
        # It means that the value is an Excel date
        # 1/1/1900 is a standard for Excel
        date_format = datetime.datetime(1900, 1, 1) + datetime.timedelta(days=test_name - 2)
        return date_format.strftime('%d-%m-%Y')
    # If it is .xlsx then the date is datetime with %H:%M:%S
    elif isinstance(test_name, datetime.datetime):
        return test_name.strftime("%d-%m-%Y")
    return test_name


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


def find_max_col_index(sheet):
    i = 3
    while i < sheet.max_column:
        if sheet.cell(3, i).value is None:
            break
        else:
            i += 1
    return i
