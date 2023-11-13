import xlrd
from openpyxl import Workbook


def parse_file(file_path):
    """
    As openpyxl doesn't support .xls, we will read and parse the file with xlrd,
    and then we will store the result of the parsing inside an openpyxl workbook
    """

    workbook_xls = xlrd.open_workbook(file_path)
    workbook = Workbook()

    """ 
    In the file we have a worksheet that contains the students' name, this
    This sheet is then used in order to copy the names in other sheets, for an
    easier data analysis we will retrieve theses name during the parsing and replace
    them in the sheets as we copy the datas
    """

    name_sheet = workbook_xls.sheet_by_name("Nom")

    # There are useless lines in the file, and we want to find the index of the
    # last row containing useful datas. We will also retrieve the students
    break_index_row, students = find_blank_index(name_sheet)

    class_name = name_sheet.cell_value(0, 0)

    # We will also delete the sheets that are useless
    for sheet in workbook_xls.sheets():

        if sheet.name in ["Nom", "B1", "B2", "Noel", "B3", "B4", "Exam. Juin"]:
            worksheet = workbook.create_sheet(title=sheet.name)

            break_index_col = 0

            if sheet.name == "Nom":
                # The only information in the names' sheet is the names and so it stops at col 2
                break_index_col += 2
            else:
                # We want to find "Total SSFL" or a blank index in order to prune the sheet
                break_index_col += find_total_or_blank_index(sheet)

            for row in range(break_index_row):
                row_data = []
                for col in range(break_index_col):
                    # If the cell contains a number
                    row_data.append(sheet.cell_value(row, col))

                    # A solution consists of checking the type of the cell in order
                    # to replace the empty cells, but I prefer to use dropna or fillna
                    # from pandas later when I turn the workbook into dataframes

                worksheet.append(row_data)

            for student in students:
                worksheet['B' + str(student[0])] = student[1]

            worksheet['A1'] = class_name
        else:
            pass

        default_sheet = workbook["Sheet"]
        workbook.remove(default_sheet)

        return workbook


def find_blank_index(name_sheet):
    # The row before this index doesn't contain names
    i = 3
    students = []
    while i < name_sheet.nrows:
        # The names are stored in the column with index 1
        if name_sheet.cell_value(i, 1) == "":
            return i, students
        else:
            students.append((i + 1, name_sheet.cell_value(i, 1)))
            i += 1


def find_total_or_blank_index(sheet):
    # We start in the third col to avoid the class columns
    i = 2
    while i < sheet.ncols:
        if sheet.cell_value(0, i) == "Total SSFL" or sheet.cell_value(0, i) == "":
            return i
        else:
            i += 1
