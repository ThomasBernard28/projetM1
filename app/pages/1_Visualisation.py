import sys

sys.path.append("..")

from app import normalizer, plotter
import streamlit as st


def initialize_page():
    st.title("Visualisation des résultats")
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Visualisation"])


def display(_plot, container):
    chart_specs = _plot.to_specs()
    container.vega_lite_chart(chart_specs, use_container_width=True)


if hasattr(st.session_state, 'normalized_df'):
    page = initialize_page()

    if page == "Visualisation":
        st.session_state.name_list = st.session_state.normalized_df["Name"].unique()

        tab1, tab2= st.tabs(["Visualisation Globale", "Visualisation par élève"])

        with tab1:
            st.header("Visualisation Globale")
            global_plot_container = st.empty()
            if not hasattr(st.session_state, 'global_plot'):
                st.session_state.global_plot = plotter.Plotter(st.session_state.normalized_df)

            display(st.session_state.global_plot, global_plot_container)

        with tab2:

            st.session_state.periods = st.session_state.normalized_df["Period"].unique().tolist()
            st.session_state.competences = st.session_state.normalized_df["Competence"].unique().tolist()

            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("Sélection des élèves")
                with st.expander("Afficher la sélection"):
                    selected_students = st.multiselect(
                        "Elèves à afficher",
                        st.session_state.name_list,
                        placeholder="Sélectionnez un ou plusieurs élèves"
                    )

            with col2:
                st.write("Options de filtrage")
                with st.expander("Afficher les options"):
                    col21, col22 = st.columns([1, 1])

                    with col21:
                        selected_periods = st.multiselect(
                            "Périodes à afficher",
                            st.session_state.periods,
                            placeholder="Sélectionnez une ou plusieurs périodes"
                        )
                        show_means = st.checkbox("Afficher la moyenne", False)

                    with col22:
                        selected_competences = st.multiselect(
                            "Compétences à afficher",
                            st.session_state.competences,
                            placeholder="Sélectionnez une ou plusieurs compétences"
                        )
                        show_quartiles = st.checkbox("Afficher les quartiles", False)

            student_plot_container = st.empty()

            if not hasattr(st.session_state, 'student_plot'):
                st.session_state.student_df = normalizer.get_all_student_results(st.session_state.normalized_df,
                                                                                 selected_students)
                st.session_state.student_plot = plotter.Plotter(st.session_state.student_df)
                display(st.session_state.student_plot, student_plot_container)

            if selected_students or show_means or show_quartiles or selected_periods or selected_competences:
                st.session_state.student_df = normalizer.get_all_student_results(st.session_state.normalized_df,
                                                                                 selected_students)

                if selected_periods:
                    st.session_state.student_df = normalizer.get_results_by_period(st.session_state.student_df,
                                                                                   selected_periods)

                if selected_competences:
                    st.session_state.student_df = normalizer.get_student_results_by_competence(
                        st.session_state.student_df, selected_competences)

                st.session_state.student_plot = plotter.Plotter(st.session_state.student_df, show_means,
                                                                st.session_state.normalized_df, selected_periods,
                                                                selected_competences, show_quartiles)
                display(st.session_state.student_plot, student_plot_container)

            if not show_means and selected_students:
                st.session_state.student_plot.hide_means()
                display(st.session_state.student_plot, student_plot_container)
