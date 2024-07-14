import streamlit as st
import fitz  # PyMuPDF for PDF handling
from docx import Document  # docx for Word document creation

st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()
def convert_pdf_to_docx(uploaded_pdf):
    pdf_bytes = uploaded_pdf.getvalue()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    docx_doc = Document()

    for page in doc:
        text = page.get_text("txt")  # Extract text in plain text format
        docx_doc.add_paragraph(text)

    return docx_doc

def main():
    st.title("PDF to Word Converter")
    uploaded_file = st.file_uploader("Upload your PDF file:", type=["pdf"])

    if uploaded_file is not None:
        try:
            converted_docx = convert_pdf_to_docx(uploaded_file)

            # Create a temporary in-memory file object (using io.BytesIO)
            from io import BytesIO
            docx_io = BytesIO()

            # Save the converted document to the in-memory file object
            converted_docx.save(docx_io)

            with st.expander("Download Converted Word Document"):
                href = st.download_button(
                    label="Download Word Document",
                    data=docx_io.getvalue(),  # Use getvalue() to retrieve the byte stream
                    file_name="converted.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
