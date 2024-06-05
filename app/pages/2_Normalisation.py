import sys

sys.path.append("..")

from app import normalizer, plotter
import streamlit as st


def initialize_page():
    st.title("Normalisation des résultats")
    return "Normalisation"


def display(_plot, container):
    chart_specs = _plot.to_specs()
    container.vega_lite_chart(chart_specs, use_container_width=True)


if hasattr(st.session_state, 'normalized_df'):
    page = initialize_page()

    if page == "Normalisation":
        st.session_state.name_list = st.session_state.normalized_df["Name"].unique()
        st.session_state.periods = st.session_state.normalized_df["Period"].unique().tolist()
        st.session_state.competences = st.session_state.normalized_df["Competence"].unique().tolist()
        st.session_state.tests = st.session_state.normalized_df["Test"].unique().tolist()
        st.session_state.class_means_df = normalizer.get_class_mean_by_test(st.session_state.normalized_df)
        st.session_state.all_student_results = normalizer.get_all_student_results(st.session_state.normalized_df,
                                                                                  st.session_state.name_list)

        tab1, tab2, tab3 = st.tabs(["Normalisation par rapport à la classe",
                                    "Normalisation par rapport à l'élève",
                                    "Normalisation par rapport à une compétence"])

        with tab1:
            st.header("Normalisation par rapport à la classe")

            class_plot_container = st.empty()

            col1, col2 = st.columns([1, 1])

            with col1:
                selected_student = st.selectbox(
                    "Elève concerné",
                    st.session_state.name_list,
                    index=None,
                    placeholder="Sélectionnez un élève"
                )
                col11, col12 = st.columns([1, 1])
                with col11:
                    show_mean = st.checkbox(label="Afficher la moyennes de classe", value=False, key="mean1")
                with col12:
                    show_quartiles = st.checkbox(label="Afficher les quantiles de classe", value=False, key="quartiles1")

            with col2:
                selected_tests = st.multiselect(
                    "Tests à normaliser",
                    st.session_state.tests,
                    placeholder="Sélectionnez le ou les tests à normaliser"
                )
                all_tests = st.checkbox(label="Sélectionner tous les tests", value=False)

            if selected_student and (selected_tests or all_tests):
                if all_tests:
                    tests = st.session_state.tests
                else:
                    tests = selected_tests

                st.session_state.normalized_class_df = normalizer.normalize_regarding_class(
                    st.session_state.all_student_results,
                    st.session_state.class_means_df)

                student_df = st.session_state.normalized_class_df[
                    (st.session_state.normalized_class_df['Name'] == selected_student)
                    & (st.session_state.normalized_class_df['Test'].isin(tests))]

                other_students_df = st.session_state.normalized_class_df[
                    (st.session_state.normalized_class_df['Name'] != selected_student)
                    & (st.session_state.normalized_class_df['Test'].isin(tests))]

                st.session_state.normalized_class_plot = plotter.Plotter(st.session_state.normalized_class_df,
                                                                         student_df, other_students_df)

                if show_mean:
                    st.session_state.normalized_class_plot.show_means(st.session_state.normalized_df)
                if show_quartiles:
                    st.session_state.normalized_class_plot.show_quartiles(st.session_state.normalized_df)

                display(st.session_state.normalized_class_plot, class_plot_container)

        with tab2:
            st.header("Normalisation par rapport à l'élève")

            student_plot_container = st.empty()

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                selected_student = st.selectbox(
                    "Elève à afficher",
                    st.session_state.name_list,
                    index=None,
                    placeholder="Sélectionnez un élève"
                )
                outliers = st.checkbox(label="Ne pas tenir compte des résultat extrêmes", value=False, key="outliers2")
            with col2:
                selected_periods = st.multiselect(
                    "Périodes à afficher",
                    st.session_state.periods,
                    placeholder="Sélectionnez une ou plusieurs périodes"
                )
                show_mean = st.checkbox("Afficher la moyenne de la classe", False, key="mean2")

            with col3:
                selected_competences = st.multiselect(
                    "Compétences à afficher",
                    st.session_state.competences,
                    placeholder="Sélectionnez une ou plusieurs compétences"
                )
                show_quartiles = st.checkbox("Afficher les quantiles de classe", False, key="quartiles2")

            if selected_student:
                st.session_state.normalized_student_df = normalizer.normalize_regarding_past_results(
                    st.session_state.normalized_df, [selected_student], outliers)

                st.session_state.class_means_df = st.session_state.normalized_df

                if selected_periods:
                    st.session_state.normalized_student_df = normalizer.get_results_by_period(
                        st.session_state.normalized_student_df, selected_periods)
                    st.session_state.class_means_df = normalizer.get_results_by_period(
                        st.session_state.class_means_df, selected_periods)

                if selected_competences:
                    st.session_state.normalized_student_df = normalizer.get_student_results_by_competence(
                        st.session_state.normalized_student_df, selected_competences)
                    st.session_state.class_means_df = normalizer.get_student_results_by_competence(
                        st.session_state.class_means_df, selected_competences)

                st.session_state.normalized_student_plot = plotter.Plotter(st.session_state.normalized_student_df,
                                                                           st.session_state.normalized_df,
                                                                           selected_periods, selected_competences)

                if show_mean:
                    st.session_state.normalized_student_plot.show_means(st.session_state.class_means_df)
                if show_quartiles:
                    st.session_state.normalized_student_plot.show_quartiles(st.session_state.class_means_df)

                display(st.session_state.normalized_student_plot, student_plot_container)

        with tab3:
            st.header("Normalisation pour un élève par rapport à une compétence")

            competence_plot_container = st.empty()

            col1, col2 = st.columns([1, 1])

            with col1:
                selected_student = st.selectbox(
                    "Élève concerné",
                    st.session_state.name_list,
                    index=None,
                    placeholder="Sélectionnez un élève"
                )
                outliers = st.checkbox(label="Ne pas tenir compte des résultat extrêmes", value=False, key="outliers")

            with col2:
                selected_competence = st.selectbox(
                    "Compétence désirée",
                    st.session_state.competences,
                    index=None,
                    placeholder="Sélectionnez une compétence"
                )
                col21, col22 = st.columns([1, 1])
                with col21:
                    show_mean = st.checkbox(label="Afficher la moyenne de classe", value=False, key="mean3")
                with col22:
                    show_quartiles = st.checkbox(label="Afficher les quantiles de classe", value=False, key="quartiles3")

            if selected_student and selected_competence:
                st.session_state.normalized_competence_df = normalizer.normalize_regarding_competence(
                    st.session_state.normalized_df,
                    selected_student,
                    selected_competence, outliers)

                st.session_state.normalized_competence_plot = plotter.Plotter(st.session_state.normalized_competence_df,
                                                                              selected_competence,
                                                                              st.session_state.normalized_df)

                st.session_state.class_means_df = normalizer.get_student_results_by_competence(
                    st.session_state.normalized_df,
                    [selected_competence])

                if show_mean:
                    st.session_state.normalized_competence_plot.show_means(st.session_state.class_means_df)
                if show_quartiles:
                    st.session_state.normalized_competence_plot.show_quartiles(st.session_state.class_means_df)

                display(st.session_state.normalized_competence_plot, competence_plot_container)
