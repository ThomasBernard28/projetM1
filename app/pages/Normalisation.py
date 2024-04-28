import sys

sys.path.append("..")

from app import normalizer, plotter
import streamlit as st


def initialize_page():
    st.title("Normalisation des résultats")
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Normalisation"])


def display(_plot, container):
    chart_specs = _plot.to_specs()
    container.vega_lite_chart(chart_specs, use_container_width=True)

if hasattr(st.session_state, 'normalized_df'):
    page = initialize_page()

    if page == "Normalisation":
        st.session_state.name_list = st.session_state.normalized_df["Name"].unique()
        st.session_state.periods = st.session_state.normalized_df["Period"].unique().tolist()
        st.session_state.competences = st.session_state.normalized_df["Competence"].unique().tolist()

        tab1, tab2, tab3 = st.tabs(["Normalisation par rapport à l'élève",
                                    "Normalisation par rapport à la classe",
                                    "Normalisation par rapport à une compétence"])

        with tab1:
            st.header("Normalisation par rapport à l'élève")


            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                selected_student = st.selectbox(
                    "Elève à afficher",
                    st.session_state.name_list,
                    index=0,
                    placeholder="Sélectionnez un élève"
                )
            with col2:
                selected_periods = st.multiselect(
                    "Périodes à afficher",
                    st.session_state.periods,
                    placeholder="Sélectionnez une ou plusieurs périodes"
                )

            with col3:
                selected_competences = st.multiselect(
                    "Compétences à afficher",
                    st.session_state.competences,
                    placeholder="Sélectionnez une ou plusieurs compétences"
                )

            st.divider()
            student_plot_container = st.empty()

            if not hasattr(st.session_state, 'normalized_student_plot'):
                st.session_state.normalized_student_plot = plotter.Plotter(st.session_state.normalized_df, True)

            display(st.session_state.normalized_student_plot, student_plot_container)

            if selected_student:
                st.session_state.normalized_student_df = normalizer.normalize_regarding_past_results(st.session_state.normalized_df, [selected_student])

                if selected_periods:
                    st.session_state.normalized_student_df = normalizer.get_results_by_period(st.session_state.normalized_student_df, selected_periods)

                if selected_competences:
                    st.session_state.normalized_student_df = normalizer.get_student_results_by_competence(st.session_state.normalized_student_df, selected_competences)

                st.session_state.normalized_student_plot = plotter.Plotter(st.session_state.normalized_student_df,
                                                                           st.session_state.normalized_df,
                                                                           selected_periods, selected_competences)
