import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import os
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

# Helper function to convert PDF to images
def pdf_to_images(pdf_file):
    images = []
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images


# Helper function to save images and zip them
def save_images_as_zip(images, base_filename):
    # Create a directory to temporarily store images
    temp_dir = f"{base_filename}_images"
    os.makedirs(temp_dir, exist_ok=True)

    # Save each image in the directory
    image_paths = []
    for i, img in enumerate(images):
        image_path = os.path.join(temp_dir, f"{base_filename}_page_{i + 1}.png")
        img.save(image_path)
        image_paths.append(image_path)

    # Create a zip file
    zip_filename = f"{base_filename}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for image_path in image_paths:
            zipf.write(image_path, os.path.basename(image_path))

    # Clean up the temporary image files
    for image_path in image_paths:
        os.remove(image_path)
    os.rmdir(temp_dir)

    return zip_filename


# Streamlit Web App
def main():
    st.title("PDF to Image Converter with Zip Download")

    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"Processing file: {uploaded_file.name}")
            images = pdf_to_images(uploaded_file)

            # Create a zip filename with the current date and time
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"{os.path.splitext(uploaded_file.name)[0]}_{current_datetime}"

            zip_filename = save_images_as_zip(images, base_filename)

            # Provide a link to download the zip file
            with open(zip_filename, "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP",
                    data=fp,
                    file_name=zip_filename,
                    mime="application/zip"
                )

            # Clean up the zip file after download link is created
            os.remove(zip_filename)


if __name__ == "__main__":
    main()
