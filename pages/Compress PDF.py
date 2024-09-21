import streamlit as st
import pandas as pd
import pdfkit
import os
import zipfile
from datetime import datetime

def convert_to_pdf(file):
    # Convert Excel file to PDF
    pdf_path = os.path.splitext(file.name)[0] + ".pdf"
    pdfkit.from_file(file.name, pdf_path)
    return pdf_path

def create_zip(pdf_paths):
    # Create a zip file with the current date and time in the filename
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"converted_files_{now}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zip_file:
        for pdf_path in pdf_paths:
            zip_file.write(pdf_path)
    return zip_filename

st.title("Excel to PDF Converter")

uploaded_files = st.file_uploader("Choose Excel files", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    pdf_paths = []
    with st.spinner("Converting files to PDF..."):
        for file in uploaded_files:
            pdf_path = convert_to_pdf(file)
            pdf_paths.append(pdf_path)
    st.success("Files converted successfully!")

    zip_filename = create_zip(pdf_paths)
    st.download_button(
        label="Download ZIP",
        data=open(zip_filename, "rb"),
        file_name=zip_filename,
        mime="application/zip",
    )

    for pdf_path in pdf_paths:
        os.remove(pdf_path)
    os.remove(zip_filename)