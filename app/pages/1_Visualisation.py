import sys

sys.path.append("..")

from app import normalizer, plotter
import streamlit as st

def initialize_page():
    """
    This method initializes the page and returns the selected page
    :return: The name of the selected page
    """
    st.title("Visualisation des résultats")
    return "Visualisation"


def display(_plot, container):
    """
    This method is used to display the plot. To do so, it uses the container to display the plot
    :param _plot:  object ot display
    :param container: The container to display the plot
    """
    chart_specs = _plot.to_specs()
    container.vega_lite_chart(chart_specs, use_container_width=True)


if hasattr(st.session_state, 'normalized_df'):
    page = initialize_page()

    if page == "Visualisation":
        st.session_state.name_list = st.session_state.normalized_df["Name"].unique()

        tab1, tab2 = st.tabs(["Visualisation Globale", "Visualisation par élève"])

        with tab1:
            st.header("Visualisation Globale")
            global_plot_container = st.empty()
            points = st.checkbox(label="Afficher la répartition des points", value=False)
            if not hasattr(st.session_state, 'global_plot'):
                st.session_state.global_plot = plotter.Plotter(st.session_state.normalized_df)

            # Options to show the class repartition
            if points:
                student_df = normalizer.get_all_student_results(st.session_state.normalized_df, st.session_state.name_list)
                st.session_state.global_plot.show_points(student_df)

            elif not points:
                st.session_state.global_plot.hide_points()

            display(st.session_state.global_plot, global_plot_container)

        with tab2:

            st.session_state.periods = st.session_state.normalized_df["Period"].unique().tolist()
            st.session_state.competences = st.session_state.normalized_df["Competence"].unique().tolist()

            student_plot_container = st.empty()

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
                        show_quartiles = st.checkbox("Afficher les quantiles", False)

            # If there is a selection in the filters then we update the plot and display it
            if selected_students or show_means or show_quartiles or selected_periods or selected_competences:
                st.session_state.student_df = normalizer.get_all_student_results(st.session_state.normalized_df,
                                                                                 selected_students)

                # Filter on the selected periods
                if selected_periods:
                    st.session_state.student_df = normalizer.get_results_by_period(st.session_state.student_df,
                                                                                   selected_periods)

                # Filter on the selected competences
                if selected_competences:
                    st.session_state.student_df = normalizer.get_student_results_by_competence(
                        st.session_state.student_df, selected_competences)

                st.session_state.student_plot = plotter.Plotter(st.session_state.student_df, show_means,
                                                                st.session_state.normalized_df, selected_periods,
                                                                selected_competences, show_quartiles)
                display(st.session_state.student_plot, student_plot_container)
