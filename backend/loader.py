import xlsLoader as xl
import xlsxLoader as xlx


def load_file(file_path, xls=False):
    if xls:
        return xl.convert_to_xlsx(file_path)
    else:
        return xlx.parse_file(file_path)

