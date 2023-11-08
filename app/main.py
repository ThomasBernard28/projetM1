import streamlit as st
from workspace import *


st.set_page_config(
    page_title="Report visualization app",
)

st.write("# Welcome to the report visualization app ! 👋")

try:
    uploaded_file = st.file_uploader("Please choose the report you want to load\n Be aware that .xls files will be "
                                     "automatically cache converted in .xlsx", type=["xls", "xlsx"])

except:
    wrong_format_exception = IOError('The file format must be .xls or .xlsx')
    st.exception(wrong_format_exception)

if uploaded_file is not None:
    workspace = Workspace(uploaded_file)
    workspace.get_student_results("Jade")
    st.write(workspace.students)
