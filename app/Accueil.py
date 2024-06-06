import os
import gc
import time
import streamlit as st
import parser
import normalizer
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Application de visualisation de résultats scolaires",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenue")

uploaded_file = st.file_uploader("Choisissez le bulletin que vous voulez exploiter", type=["xls", "xlsx"], )

if uploaded_file is not None:
    suffix = ".xls" if uploaded_file.name.endswith(".xls") else ".xlsx"
    with NamedTemporaryFile(dir="../resources/", delete=False, suffix=suffix) as file:
        file.write(uploaded_file.getbuffer())
        file_path = file.name  # Retain the file path after closing the block

    try:
        periods = parser.get_periods(file_path, uploaded_file.name.endswith(".xls"))

        with st.form("periods form"):
            st.write("Sélecteur de périodes")
            selected_periods = st.multiselect(
                "Périodes à prendre en compte",
                periods,
                placeholder="Sélectionnez une ou plusieurs périodes à prendre en compte",
                default=periods
            )
            button = st.form_submit_button("Valider")
            if button:
                st.session_state.df = parser.parse_file(file_path, uploaded_file.name.endswith(".xls"), selected_periods)

        if hasattr(st.session_state, 'df'):
            normalized_df = normalizer.normalize_results(st.session_state.df)
            st.write("Données chargées ✅\n Vous pouvez vous rendre sur la page de visualisation")
            st.session_state.normalized_df = normalized_df
            st.sidebar.success("Fichier chargé!")
    finally:
        gc.collect()
        time.sleep(1)  # Ensure no lingering handles
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            st.warning("Temporary file not found for deletion.")
