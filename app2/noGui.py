import parser
import pandas as pd


file_path = "../resources/bulletin.xls"

dataframe = parser.parse_file(file_path, True)

print(dataframe)