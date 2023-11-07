import os
from tempfile import NamedTemporaryFile
import streamlit as st
import backend.loader as loader


class Workspace:

    def __init__(self, st_uploaded_file):
        self.workbook = None

        if st_uploaded_file.name.endswith(".xls"):
            with NamedTemporaryFile(dir="/resources/", delete=False, suffix=".xls") as file:
                file.write(st_uploaded_file.getbuffer())
                self.workbook = loader.load_file(file.name, True)
            os.remove(file.name)

        else:
            with NamedTemporaryFile(dir="/resources/", delete=False, suffix=".xlsx") as file:
                file.write(st_uploaded_file.getbuffer())
                self.workbook = loader.load_file(file.name, True)
            os.remove(file.name)
