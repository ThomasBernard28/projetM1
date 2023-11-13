import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Report visualization app",
    page_icon="📈",
)

st.write("""
# Report Visualization Application 📈

The first thing you have to do is just loading a file into the file loader

""")

selected2 = option_menu(None, ["Home", "Uploader", "Class Overall", "Individual"],
    icons=['house', 'file-earmark-bar-graph', 'people', 'person'],
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2
