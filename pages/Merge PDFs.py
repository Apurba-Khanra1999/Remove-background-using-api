import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO
from datetime import datetime
import time


st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()

# Function to merge PDFs
def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merged_pdf = BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    return merged_pdf


# Function to generate the filename with the current timestamp
def generate_filename():
    return f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"


# Streamlit app
st.title("Merge multiple PDFs")

uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

if uploaded_files:
    st.write("Select the order of the PDFs to be merged:")

    # Display file names and allow users to select the order
    file_names = [file.name for file in uploaded_files]
    selected_order = st.multiselect("Order of PDFs", file_names, default=file_names)

    if len(selected_order) != len(file_names):
        st.warning("Please select all PDFs in the desired order.")
    else:
        # Reorder the uploaded files based on user selection
        ordered_files = [uploaded_files[file_names.index(name)] for name in selected_order]

        # Displaying loader while processing the files
        with st.spinner('Merging PDFs...'):
            time.sleep(1)  # Simulate a brief delay
            merged_pdf = merge_pdfs(ordered_files)

        st.success("PDF files merged successfully!")

        # Adding a delay to simulate download processing time
        with st.spinner('Preparing download...'):
            time.sleep(1)

        # Generating filename with timestamp
        filename = generate_filename()

        # Download button for the merged PDF
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf,
            file_name=filename,
            mime="application/pdf"
        )
