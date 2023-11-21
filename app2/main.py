import os

import streamlit as st
import parser
from tempfile import NamedTemporaryFile


st.set_page_config(
    page_title="Report visualization app 📈 "
)

try:
    uploaded_file = st.file_uploader("Please choose the report file you want to load", type=["xls", "xlsx"])
except:
    e = FileNotFoundError("The file wasn't found")
    st.exception(e)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".xsl"):
        # delete = True supported on Linux and MacOS but not on Windows so os.remove() is used instead
        # As streamlit transform the file to a buffer, a temporary file is needed
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
            file.write(uploaded_file.getbuffer())
            df = parser.parse_file(file.name, True)
            st.write(df)
        os.remove(file.name)

    else:
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
            file.write(uploaded_file.getbuffer())
            df = parser.parse_file(file.name, True)
            st.write(df)
        os.remove(file.name)
