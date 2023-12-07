import sys
sys.path.append("..")
from app import plotter, normalizer
import streamlit as st

if hasattr(st.session_state, 'normalized_df'):
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Visualization"])

    if page == "Visualization":
        st.title("Report Visualization")

        name_list = st.session_state.normalized_df['Name'].unique().tolist()

        selected_students = st.multiselect(
            'Select one or more students',
            name_list,
        )

        st.divider()

        hide_means = False

        base_plot = plotter.Plotter(st.session_state.normalized_df)
        base_plot.plot(base_plot.chart)

        def insert_student_in_chart(students, _plot):
            if len(students) >= 1:
                student_df = normalizer.get_all_student_results(st.session_state.normalized_df, students)
                _plot.add_students(student_df)
                final_chart = _plot.chart
                _plot.plot(final_chart)

        insert_student_in_chart(selected_students, base_plot)