import streamlit as st
from pikepdf import Pdf
import os
import tempfile
import shutil


def compress_pdf(file, quality):
    input_pdf = Pdf.open(file)

    # Create a temporary file for the compressed PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file_path = temp_file.name

    # Simulate compression by lowering the quality parameter
    compression_quality = (100 - quality) / 100

    # Save the PDF to the temporary file
    with Pdf.new() as output_pdf:
        for page in input_pdf.pages:
            output_pdf.pages.append(page)
        output_pdf.save(temp_file_path, compress_streams=True)

    # Return the path and file size
    file_size = os.path.getsize(temp_file_path)
    return temp_file_path, file_size


def main():
    st.title("PDF Compressor")

    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if pdf_file is not None:
        quality = st.slider("Select Compression Quality", 1, 100, 50)

        if st.button("Compress PDF"):
            with st.spinner("Compressing..."):
                compressed_file, file_size = compress_pdf(pdf_file, quality)
                st.success("Compression Complete!")
                st.write(f"Approximate File Size: {file_size / 1024:.2f} KB")

                # Provide download link
                with open(compressed_file, "rb") as f:
                    st.download_button(
                        label="Download Compressed PDF",
                        data=f,
                        file_name=os.path.basename(compressed_file),
                        mime="application/pdf"
                    )

                # Clean up temporary file
                os.remove(compressed_file)


if __name__ == "__main__":
    main()
