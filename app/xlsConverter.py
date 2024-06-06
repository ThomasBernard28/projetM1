import xlrd
from openpyxl import Workbook


def get_periods(file_path):
    workbook = xlrd.open_workbook_xls(file_path)
    return workbook.sheet_names()


def convert_to_xlsx(file_path):
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
