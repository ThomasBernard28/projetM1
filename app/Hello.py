import os
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

uploaded_file = st.file_uploader("Choisissez le bulletin que vous voulez exploiter", type=["xls", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".xls"):
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
            file.write(uploaded_file.getbuffer())
            df = parser.parse_file(file.name, True)
    else:
        with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
            file.write(uploaded_file.getbuffer())
            df = parser.parse_file(file.name, False)
    os.remove(file.name)

    normalized_df = normalizer.normalize_results(df)
    st.write("Données chargées ✅\n Vous pouvez vous rendre sur la page de visualisation")

    # Save the normalized_df to use it in other pages
    st.session_state.normalized_df = normalized_df

    # Redirect to the next page
    st.sidebar.success("Fichier chargé! Rendez vous à la page de visualisation.")
