import streamlit as st
import dataLoader as dl
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Report visualization app",
    page_icon="👋",
)

st.write("# Welcome to the report visualisation app, this is the main page! 👋")

uploaded_file = st.file_uploader("Please choose the report you want to load")
if uploaded_file is not None:
    with NamedTemporaryFile(dir="../resources/") as file:
        file.write(uploaded_file.getbuffer())
        wb = dl.load_file(file.name)
        st.write(dl.get_a_dataframe_by_sheet(wb, "B1"))

