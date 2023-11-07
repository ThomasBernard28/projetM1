import os
import streamlit as st
import xlsLoader as xl
import xlsxLoader as xlx
import dataExplorer as de
import matplotlib.pyplot as plt

from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Report visualization app",
    page_icon="👋",
)

st.write("# Welcome to the report visualisation app, this is the main page! 👋")

try:
    uploaded_file = st.file_uploader("Please choose the report you want to load", type=["xls", "xlsx"])

except:
    raise Exception("The file format must be .xls or .xlsx")


# This function is used to call the loaders functions
def load_file(file_path, xls=False):
    if xls:
        return xl.convert_to_xlsx(file_path)
    else:
        return xlx.parse_file(file_path)


if uploaded_file is not None:
    # We check the extension of the file which must be .xls or .xlsx
    if uploaded_file.name.endswith(".xls"):
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
            file.write(uploaded_file.getbuffer())
            wb = load_file(file.name, True)
            df = de.get_student_results_from_one_sheet(wb,"Camille", "B2")
            st.line_chart(df.set_index('Test Number')['Results'])
        os.remove(file.name)

    else:
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
            file.write(uploaded_file.getbuffer())
            wb = load_file(file.name, False)
            st.write(de.get_a_dataframe_by_sheet(wb, "B3"))
        os.remove(file.name)
