import pandas as pd
import openpyxl
import xlsLoader as xls2
import xlsxLoader as xlsx2


def load_file(file, is_xls):
    if is_xls:
        workbook = xls2.parse_file(file)

    else:
        workbook = xlsx2.parse_file(file)
