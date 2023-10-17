import openpyxl
import xlrd


def loadFile(file_path):
    try:
        wb = openpyxl.load_workbook(file_path)
        return wb
    except:
        # The xlsx doesn't exist yet
        wb = convertToXlsx(file_path)
        return wb


def convertToXlsx(file_path):
    # As openpyxl doesn't support .xls we will convert it to .xlsx
    workbook_xls = xlrd.open_workbook(file_path)
    wb = openpyxl.Workbook()

    # I use the nameSheet blank index of the name sheet because the list of marks stops after the last student
    nameSheet = workbook_xls.sheet_by_name("Nom")
    break_index_row = findBlanklIndex(nameSheet)

    # We will also delete useless sheets and useless infos
    for sheet_xls in workbook_xls.sheets():
        if sheet_xls.name in ["Nom", "B1", "B2", "Noel", "B3", "B4", "Exam. Juin"]:
            ws = wb.create_sheet(title=sheet_xls.name)

            break_index_col = 0

            if sheet_xls.name != "Nom":
                break_index_col += findTotalOrBlankIndex(sheet_xls)

            else:
                break_index_col += 2

            for row in range(break_index_row):
                row_data = []
                for col in range(break_index_col):
                    row_data.append(sheet_xls.cell_value(row, col))
                ws.append(row_data)
        else :
            pass
    default_sheet = wb["Sheet"]
    wb.remove(default_sheet)

    xlsx_file = "../resources/output.xlsx"
    wb.save(xlsx_file)
    return wb


def findTotalOrBlankIndex(sheet_xls):
    i = 2
    while i < sheet_xls.ncols:
        if sheet_xls.cell_value(0, i) == "Total SSFL" or sheet_xls.cell_value(0, i) == "":
            return i
        else:
            i = i + 1

def findBlanklIndex(sheet_xls):
    i = 3
    while i < sheet_xls.nrows:
        if sheet_xls.cell_value(i, 1) == "":
            print(i)
            return i
        else:
            i = i + 1

loadFile("../resources/bulletin.xls")
