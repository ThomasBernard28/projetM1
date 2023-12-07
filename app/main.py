import os

import streamlit as st
import parser
import normalizer
import altair as alt
import plotter
import pandas as pd
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Report visualization app 📈 "
)

st.title("Welcome to Report visualizer")

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

    # student_df = normalizer.get_all_student_results(normalized_df, "Jade")

    st.write("Data loaded successfully ✅ ")

    st.divider()
    name_list = normalized_df['Name'].unique().tolist()

    selected_students = st.multiselect(
        'Select one or more student',
        name_list,
    )

    st.divider()

    hide_means = False

    base_plot = plotter.Plotter(normalized_df)
    base_plot.plot(base_plot.chart)


    @st.cache_data
    def insert_student_in_chart(students, _plot):
        if len(students) >= 1:
            student_df = normalizer.get_all_student_results(normalized_df, students)
            _plot.add_students(student_df)
            if not hide_means:
                final_chart = _plot.chart

            else:
                final_chart = _plot.chart - _plot.base_chart

            _plot.plot(final_chart)

    insert_student_in_chart(selected_students, base_plot)

