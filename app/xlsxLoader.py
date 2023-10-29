from openpyxl import Workbook, load_workbook


def parse_file(file_path):
    workbook = load_workbook(file_path)
    parsed_workbook = Workbook()

    name_sheet = workbook["Nom"]
    break_index_row = find_blank_index(name_sheet)

    class_name = name_sheet.cell(1, 1).value
    students = find_all_students(name_sheet)

    sheet_names = workbook.sheetnames
    for sheet_name in sheet_names:
        if sheet_name in ["Nom", "B1", "B2", "Noel", "B3", "B4", "Exam. Juin"]:
            sheet = workbook[sheet_name]
            parsed_sheet = parsed_workbook.create_sheet(title=sheet_name)

            break_index_col = 1

            if sheet_name != "Nom":
                break_index_col += find_total_or_blank_index(sheet)

            else:
                break_index_col += 2

            for row in range(break_index_row):
                row_data = []
                for col in range(break_index_col):
                    if isinstance(sheet.cell(row, col).value, (int,float)):
                        row_data.append(sheet.cell(row, col).value)
                    elif sheet.cell(row, col).value is None and (col > 1 and row > 2):
                        row_data.append("NP")
                    else:
                        row_data.append(sheet.cell(row, col).value)

                parsed_sheet.append(row_data)

            for student in students:
                parsed_sheet['B'+str(student[0])] = student[1]

            parsed_sheet['A1'] = class_name

        else:
            pass

    default_sheet = parsed_workbook["Sheet"]
    parsed_workbook.remove(default_sheet)

    return parsed_workbook


def find_blank_index(sheet):
    i = 4
    while i < sheet.max_row:
        if sheet.cell(i, 2).value is None:
            return i


def find_all_students(sheet):
    i = 4
    students = []
    while i < sheet.max_row and sheet.cell(i, 2).value is not None:
        students.append((i + 1, sheet.cell(i, 2).value))
        i += 1
    return students


def find_total_or_blank_index(sheet):
    i = 3
    while i < sheet.max_column:
        if sheet.cell(1, i).value == "Total SSFL" or sheet.cell(1, i).value is None:
            return i
        i += 1
