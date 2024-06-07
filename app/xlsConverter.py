import xlrd
from openpyxl import Workbook

"""
This module is used to convert xls files to an openpyxl workbook which can be considered as a xlsx workbook
"""


def get_periods(file_path):
    """
    This method is used to extract the periods from a xls file
    The periods are the names of the sheets in the workbook
    :param file_path: the path to the xls file
    :return: A list of strings representing the periods
    """
    workbook = xlrd.open_workbook_xls(file_path)
    return workbook.sheet_names()


def convert_to_xlsx(file_path):
    """
    This method is used to convert a xls file to an openpyxl workbook
    By doing so the workbook can be considered as a xlsx workbook
    In order to convert the xls file, xlrd library is used to read the xls file and copy the data to an openpyxl workbook
    :param file_path: the path to the xls file
    :return: An openpyxl workbook
    """
    workbook_xls = xlrd.open_workbook_xls(file_path)
    workbook = Workbook()

    for sheet in workbook_xls.sheets():
        worksheet = workbook.create_sheet(title=sheet.name)

        for row in range(sheet.nrows):
            row_data = []
            for col in range(sheet.ncols):
                cell_value = sheet.cell_value(row, col)

                if cell_value == "":
                    row_data.append(None)

                else:
                    row_data.append(cell_value)

            worksheet.append(row_data)

    default_sheet = workbook["Sheet"]
    workbook.remove(default_sheet)

    return workbook
