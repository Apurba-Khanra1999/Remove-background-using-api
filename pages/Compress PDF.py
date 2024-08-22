import streamlit as st
import PyPDF2
import io
import zipfile
from datetime import datetime

st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()


def compress_pdf(input_file):
    reader = PyPDF2.PdfReader(input_file)
    writer = PyPDF2.PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output


st.title("PDF Compressor")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.write(f"{len(uploaded_files)} file(s) uploaded successfully!")

    if st.button("Compress PDFs"):
        # Create a buffer to hold the zip file in memory
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, uploaded_file in enumerate(uploaded_files):
                # Compress the PDF
                compressed_pdf = compress_pdf(uploaded_file)

                # Add the compressed PDF to the zip file
                pdf_name = f"compressed_{i + 1}.pdf"
                zf.writestr(pdf_name, compressed_pdf.getvalue())

        # Set the zip buffer's position to the start
        zip_buffer.seek(0)

        # Create a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"compressed_pdfs_{timestamp}.zip"

        # Offer the zip file for download
        st.download_button(
            label="Download",
            data=zip_buffer,
            file_name=zip_filename,
            mime="application/zip"
        )

st.write("Note: The compression level may vary depending on the content of the PDFs.")
