from workspace import Workspace
import normalizer as norm
import streamlit as st

st.set_page_config(
    page_title="Report visualization app"
)

workspace = None

try:
    uploaded_file = st.file_uploader("Please choose the report file you want to load", type=["xls", "xlsx"])
except:
    e = FileNotFoundError("The file wasn't found")
    st.exception(e)


if uploaded_file is not None:

    if uploaded_file.name.endswith(".xls"):
        workspace = Workspace(uploaded_file.getbuffer(), True)
        st.write(workspace.get_a_dataframe_from_sheet("B1"))
        results_of_jade = norm.get_all_student_results(workspace.dataframes, "Jade")
        print(results_of_jade)
        print(norm.get_student_results_by_period(results_of_jade, ["B1", "B2"]))

    else:
        workspace = Workspace(uploaded_file.getbuffer(), False)
        print(workspace.categories)

