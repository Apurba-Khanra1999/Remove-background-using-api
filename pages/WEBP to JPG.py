import io

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
def convert_webp_to_jpg(uploaded_file):
    try:
        # Open the uploaded file in binary mode
        image_data = uploaded_file.read()

        # Load the image using Pillow's WEBP support
        img = Image.open(io.BytesIO(image_data))

        # Convert to RGB mode (if necessary) for compatibility
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save the converted image as JPG in memory
        converted_img_data = io.BytesIO()
        img.save(converted_img_data, format='JPEG')

        return converted_img_data.getvalue()

    except OSError:
        raise ValueError("Uploaded file is not a valid WEBP image.")

st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()
st.title("WEBP to JPG Converter")
uploaded_file = st.file_uploader("Choose a WEBP image to convert:", type=['webp','png'])

if uploaded_file is not None:
    try:
        converted_data = convert_webp_to_jpg(uploaded_file)
        st.success("Conversion successful!")

        with st.expander("Download Converted JPG"):
            st.download_button("Download JPG", converted_data, file_name="converted.jpg")

    except ValueError as e:
        st.error(f"Error: {e}")

