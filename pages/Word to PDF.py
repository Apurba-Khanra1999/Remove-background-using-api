import streamlit as st
from docx2pdf import convert
from datetime import datetime
from zipfile import ZipFile
import time
import pythoncom
import os

st.set_page_config(
    page_title="word to pdf",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()

def main():
    pythoncom.CoInitialize()
    st.title("Word to PDF Converter")

    # File Uploader
    uploaded_files = st.file_uploader("Upload Word Files (.docx only)",
                                      accept_multiple_files=True,
                                      type=["docx"])

    if uploaded_files:
        st.info(f"Number of files uploaded: {len(uploaded_files)}")

        # Directory to save intermediate files
        temp_dir = "temp_dir"
        os.makedirs(temp_dir, exist_ok=True)

        # Progress bar
        progress_bar = st.progress(0)

        # If only one file is uploaded
        if len(uploaded_files) == 1:
            uploaded_file = uploaded_files[0]

            # Save the file temporarily
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            try:
                # Convert to PDF
                pdf_filename = f"converted_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
                convert(temp_path, pdf_filename)

                # Update progress bar to complete
                progress_bar.progress(100)

                # Download the PDF
                with open(pdf_filename, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error converting file: {e}")

        # If multiple files are uploaded
        else:
            zip_filename = f"converted_files_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
            with ZipFile(zip_filename, "w") as zipObj:
                for i, uploaded_file in enumerate(uploaded_files):
                    # Save each file temporarily
                    temp_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.read())

                    try:
                        # Convert to PDF
                        pdf_filename = f"converted_{i + 1}.pdf"
                        convert(temp_path, pdf_filename)

                        # Add PDF to the zip file
                        zipObj.write(pdf_filename)

                        # Update progress bar
                        progress_bar.progress((i + 1) / len(uploaded_files))
                        time.sleep(0.1)  # Simulate processing time
                    except Exception as e:
                        st.error(f"Error converting file: {e}")

            # Download the zip file
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="Download ZIP",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip"
                )

        # Clean up temporary directory
        for temp_file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, temp_file))
        os.rmdir(temp_dir)


if __name__ == "__main__":
    main()
