import sys

# In order to import from parent directory
sys.path.append("..")
from app import plotter, normalizer, plotter2
import streamlit as st


def initialize_page():
    st.title("Visualisation des résultats")
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Visualisation"])


def update_chart(_plot, students, periods):
    insert_in_chart(_plot, students, periods)


def insert_in_chart(_plot, students, periods):
    if len(students) >= 1:
        st.session_state.student_df = normalizer.get_all_student_results(st.session_state.normalized_df, students)
        if len(periods) >= 1:
            st.session_state.period_df = normalizer.get_results_by_period(st.session_state.student_df, periods)
            _plot.create_line_and_circle_chart(st.session_state.period_df)
            _plot.create_means_line_chart(periods)
        else:
            _plot.create_line_and_circle_chart(st.session_state.student_df)

    else:
        if len(periods) >= 0:
            # st.session_state.period_df = normalizer.get_results_by_period(st.session_state.normalized_df,periods)
            _plot.create_means_line_chart(periods)

    _plot.add_infos()
    display(_plot)


def filter_by_period(periods, _plot):
    if len(periods) >= 1:
        if hasattr(st.session_state, 'student_df'):
            period_df = normalizer.get_student_results_by_period(st.session_state.student_df, periods)
            _plot.by_period(period_df)
            display(_plot)
        else:
            period_df = normalizer.get_student_results_by_period(st.session_state.normalized_df,
                                                                 st.session_state.periods)
            _plot.by_period(period_df, )
            display(_plot)


def insert_student_in_chart(students, _plot):
    if len(students) >= 1:
        st.session_state.student_df = normalizer.get_all_student_results(st.session_state.normalized_df, students)

        _plot.create_line_and_circle_chart(st.session_state.student_df)
        _plot.add_students()
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

        # TODO Attention problème lorsque l'on sélectionne des périodes ça ne marche pas
        # TODO Si on enlève des élèves et que périodes sélectionnées ils ne disparaissent pas
        # TODO utiliser st.tabs pour faire des tabs avec différentes vues

        col1, col2 = st.columns([1, 2])

        with col1:
            all_students = st.checkbox("Afficher tous les élèves")
            show_means = st.checkbox("Afficher la moyenne", True)

        with col2:
            st.session_state.periods = st.session_state.normalized_df['Period'].unique().tolist()
            selected_periods = st.multiselect(
                'Sélectionnez une ou plusieurs périodes',
                st.session_state.periods
            )

        st.divider()

        plot_container = st.empty()

        if not hasattr(st.session_state, 'base_plot'):
            st.session_state.base_plot = plotter2.Plotter2(st.session_state.normalized_df)
            st.session_state.base_plot.create_means_line_chart()

        if not show_means:
            if selected_students:
                st.session_state.base_plot.hide_means()
                display(st.session_state.base_plot)

        else:
            st.session_state.base_plot.show_means()
            display(st.session_state.base_plot)

        if selected_students:
            update_chart(st.session_state.base_plot, selected_students, selected_periods)
        else:
            st.session_state.base_plot.reset_chart_to_means()
            display(st.session_state.base_plot)

        if all_students:
            update_chart(st.session_state.base_plot, st.session_state.name_list, selected_periods)

        if selected_periods:
            st.session_state.base_plot.hide_means()
            update_chart(st.session_state.base_plot, selected_students, selected_periods)
            # filter_by_period(selected_periods, st.session_state.base_plot)
        else:
            update_chart(st.session_state.base_plot, selected_students, selected_periods)
