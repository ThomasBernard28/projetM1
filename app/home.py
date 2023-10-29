import streamlit as st
import dataLoader as dl
import xlsxLoader as xl
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Report visualization app",
    page_icon="👋",
)

st.write("# Welcome to the report visualisation app, this is the main page! 👋")

uploaded_file = st.file_uploader("Please choose the report you want to load", type=["xls", "xlsx"])


def load_file(file_path, xls=False):
    if xls:
        return dl.convert_to_xlsx(file_path)
    else:
        return xl.parse_file(file_path)


if uploaded_file is not None:
    if uploaded_file.name.endswith(".xls"):
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
            file.write(uploaded_file.getbuffer())
            wb = load_file(file.name, True)
            st.write(dl.get_a_dataframe_by_sheet(wb, "B2"))
    else:
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
            file.write(uploaded_file.getbuffer())
            wb = load_file(file.name)
            st.write(dl.get_a_dataframe_by_sheet(wb, "B2"))
