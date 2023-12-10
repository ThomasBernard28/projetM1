import sys

# In order to import from parent directory
sys.path.append("..")
from app import plotter2, normalizer
import streamlit as st


def initialize_page():
    st.title("Results visualization")
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Visualization"])


def update_chart(students, base_plot):
    base_plot.plot()
    insert_student_in_chart(students, base_plot)


def insert_student_in_chart(students, _plot):
    if len(students) >= 1:
        student_df = normalizer.get_all_student_results(st.session_state.normalized_df, students)
        _plot.add_students(student_df)
        _plot.plot()


if hasattr(st.session_state, 'normalized_df'):
    page = initialize_page()

    if page == "Visualization":
        st.session_state.name_list = st.session_state.normalized_df['Name'].unique().tolist()

        st.divider()

        hide_means = False

        if not hasattr(st.session_state, 'base_plot'):
            st.session_state.base_plot = plotter2.Plotter2(st.session_state.normalized_df)

        col1, col2 = st.columns([1, 2])

        with col1:
            selected_students = st.multiselect(
                'Select one or more students',
                st.session_state.name_list,
            )

        with col2:
            if selected_students:
                update_chart(selected_students, st.session_state.base_plot)
            else:
                st.session_state.base_plot.reset()
                st.session_state.base_plot.plot()
