import os

import streamlit as st
import parser
import normalizer
import pandas as pd
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Report visualization app 📈 "
)

try:
    uploaded_file = st.file_uploader("Please choose the report file you want to load", type=["xls", "xlsx"])
except:
    e = FileNotFoundError("The file wasn't found")
    st.exception(e)
    st.write("Data not loaded successfully ❌")

if uploaded_file is not None:

    if uploaded_file.name.endswith(".xls"):
        # delete = True supported on Linux and MacOS but not on Windows so os.remove() is used instead
        # As streamlit transform the file to a buffer, a temporary file is needed
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
            file.write(uploaded_file.getbuffer())
            df = parser.parse_file(file.name, True)
        os.remove(file.name)

    else:
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
            file.write(uploaded_file.getbuffer())
            df = parser.parse_file(file.name, False)
        os.remove(file.name)

    normalized_df = normalizer.normalize_results(df)

    student_df = normalizer.get_all_student_results(normalized_df, "Jade")

    st.write("Data loaded successfully ✅ ")

    st.divider()

    st.write("Choose the whole class or some students")

    chart_data = student_df[['Test', 'Normalized', 'Period']]
    chart_data.dropna(inplace=True)
    st.write(chart_data)

    vega_lite_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "layer": [
            {
                "mark": {"type": "line", "point": True},
                "encoding": {
                    "x": {"field": "Test", "type": "ordinal", "sort": {"field": "index"}},
                    "y": {"field": "Normalized", "type": "quantitative"},

                }
            }
        ]
    }

    st.vega_lite_chart(chart_data, vega_lite_spec, use_container_width=True)