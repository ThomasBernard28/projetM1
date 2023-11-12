import os
from tempfile import NamedTemporaryFile


class Workspace:

    def __init__(self, st_uploaded_buffer, is_xls):
        """
        We take for the construction a buffer containing a that has been uploaded with
        Streamlit's file uploader and a boolean that specifies if the file
        is an .xls or .xlsx
        """

        if is_xls:
            with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xls") as file:
                file.write(st_uploaded_buffer)
            os.remove(file.name)

        else:
            with NamedTemporaryFile(dir="../resources/", delete=False, suffix=".xlsx") as file:
                file.write(st_uploaded_buffer)
            os.remove(file.name)
