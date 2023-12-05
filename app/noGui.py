import parser
import normalizer
import pandas as pd


file_path = "../resources/bulletin.xlsx"

dataframe = parser.parse_file(file_path, False)
normalized_df = normalizer.normalize_results(dataframe)
mean = normalizer.get_class_mean_by_test(normalized_df, "Test de Delphine")
print(mean)

