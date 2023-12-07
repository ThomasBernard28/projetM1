import streamlit as st
import pandas as pd
import altair as alt
import normalizer as norm


class Plotter:
    dataframe = None
    means_dataframe = None
    vega_lite_spec = None
    base_chart = None
    chart = None

    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.means_dataframe = norm.get_class_mean_by_test(self.dataframe)
        class_line_chart = alt.Chart(self.means_dataframe).mark_line(strokeDash=[4, 1]).encode(
            x="Test:O",
            y="Mean:Q",
            tooltip=['Test', 'Mean'],
            color=alt.value('white')
        ).interactive()
        class_circle_chart = alt.Chart(self.means_dataframe).mark_circle().encode(
            x="Test:O",
            y="Mean:Q",
            tooltip=['Test', 'Mean'],
            color=alt.value('white')
        ).interactive()
        self.class_line_chart = class_line_chart.properties(
            title='Class means over tests'
        )
        self.base_chart = class_circle_chart + class_line_chart
        self.chart = self.base_chart

    def plot(self, chart):
        self.vega_lite_spec = chart.to_dict()
        st.vega_lite_chart(self.vega_lite_spec, use_container_width=True)

    def add_students(self, student_df):
        student_chart = alt.Chart(student_df).mark_line().encode(
            x="Test:O",
            y="Normalized:Q",
            tooltip=['Test', 'Normalized'],
            color='Name:N'
        ).interactive()
        self.chart += student_chart
