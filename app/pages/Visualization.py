import sys

# In order to import from parent directory
sys.path.append("..")
from app import plotter, normalizer
import streamlit as st


def initialize_page():
    st.title("Visualisation des résultats")
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Visualisation"])


def update_chart(students, _plot):
    insert_student_in_chart(students, _plot)


def filter_by_period(periods, _plot):
    if len(periods) >= 1:
        if hasattr(st.session_state, 'student_df'):
            period_df = normalizer.get_student_results_by_period(st.session_state.student_df, st.session_state.periods)
            _plot.by_period(period_df)
            display(_plot)
        else:
            period_df = normalizer.get_student_results_by_period(st.session_state.normalized_df,
                                                                 st.session_state.periods)
            _plot.by_period(period_df)
            display(_plot)


def insert_student_in_chart(students, _plot):
    if len(students) >= 1:
        st.session_state.student_df = normalizer.get_all_student_results(st.session_state.normalized_df, students)
        _plot.add_students(st.session_state.student_df)
        display(_plot)


def display(_plot):
    chart_specs = _plot.tospecs()
    plot_container.vega_lite_chart(chart_specs, use_container_width=True)


if hasattr(st.session_state, 'normalized_df'):
    page = initialize_page()

    if page == "Visualisation":
        st.session_state.name_list = st.session_state.normalized_df['Name'].unique().tolist()

        selected_students = st.multiselect(
            'Sélectionnez un ou plusieurs élèves',
            st.session_state.name_list
        )

        #TODO Attention problème lorsque l'on sélectionne des périodes ça ne marche pas
        #TODO Si on enlève des élèves et que périodes sélectionnées ils ne disparaissent pas
        #TODO hint : Il faudrait modifier la gestion du graphique le problème a l'air de venir
        #TODO de l'accumulation de l'information au sein du graphe.

        col1, col2 = st.columns([1, 2])

        with col1:
            all_students = st.checkbox("Afficher tous les élèves")
            hide_means = st.checkbox("Afficher la moyenne", True)

        with col2:
            st.session_state.periods = st.session_state.normalized_df['Period'].unique().tolist()
            selected_periods = st.multiselect(
                'Sélectionnez une ou plusieurs périodes',
                st.session_state.periods
            )

        st.divider()

        plot_container = st.empty()

        if not hasattr(st.session_state, 'base_plot'):
            st.session_state.base_plot = plotter.Plotter(st.session_state.normalized_df)
            display(st.session_state.base_plot)

        if selected_students:
            update_chart(selected_students, st.session_state.base_plot)
        else:
            st.session_state.base_plot.reset()
            display(st.session_state.base_plot)

        if all_students:
            update_chart(st.session_state.name_list, st.session_state.base_plot)

        if selected_periods:
            filter_by_period(selected_periods, st.session_state.base_plot)
