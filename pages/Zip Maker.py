import streamlit as st
from zipfile import ZipFile
from io import BytesIO

st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# Function to create a zip file in memory
def create_zip(files):
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        for file_name, file_data in files.items():
            zip_file.writestr(file_name, file_data.getvalue())
    zip_buffer.seek(0)
    return zip_buffer


st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()
# Streamlit app
st.title("Zip Multiple Files")

# File uploader
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

if uploaded_files:
    files = {uploaded_file.name: uploaded_file for uploaded_file in uploaded_files}

    if st.button("Create Zip"):
        zip_buffer = create_zip(files)

        st.download_button(
            label="Download Zip",
            data=zip_buffer,
            file_name="files.zip",
            mime="application/zip"
        )
