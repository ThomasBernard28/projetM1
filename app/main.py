import os

import streamlit as st
import parser
import normalizer
import altair as alt
import ploter
import pandas as pd
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Report visualization app 📈 "
)

st.title("Welcome to the report visualisation app")

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

    means_df = normalizer.get_class_mean_by_test(normalized_df)

    #vega_lite_spec = ploter.default_plot(means_df)

    student_df = normalizer.get_all_student_results(normalized_df, "Jade")

    st.write("Data loaded successfully ✅ ")

    st.divider()
    name_list = normalized_df['Name'].unique().tolist()
    options = ['All'] + name_list

    selected_students = st.multiselect(
        'Select one or more student',
        options,
        ['All']
    )

    st.divider()


    if len(selected_students) >= 1:
        for student in selected_students:
            if student != "All":
                pass

            else:
                pass

    #st.vega_lite_chart(means_df, vega_lite_spec, use_container_width=True)
    circle_chart = alt.Chart(means_df).mark_circle().encode(
        x='Test:O',
        y='Mean:Q',
        tooltip=['Test', 'Mean'],
        color=alt.value('white')
    ).interactive()

    line_chart = alt.Chart(means_df).mark_line(strokeDash=[5, 2]).encode(
        x='Test:O',
        y='Mean:Q',
        tooltip=['Test', 'Mean'],
        color=alt.value('white')
    ).interactive()

    student_chart = alt.Chart(student_df).mark_line().encode(
        x='Test:O',
        y='Normalized:Q',
        tooltip=['Test', 'Normalized'],
        color='Name:N'
    ).interactive()

    chart = circle_chart + line_chart + student_chart

    chart = chart.properties(
        title='Class mean over the tests'
    )

    #TODO: Rework le get student results pour accepter de multiples étudiants
    #TODO: Rework le desing de l'app pour changer de page une fois la feuille chargée
    #TODO: Gérer la création des plots dans le fichier ploter.

    vega_lite_spec = chart.to_dict()

    st.vega_lite_chart(vega_lite_spec, use_container_width=True)