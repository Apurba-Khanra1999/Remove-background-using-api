import streamlit as st
from PIL import Image
import io
st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
def convert_to_webp(image_data):
  image = Image.open(io.BytesIO(image_data))
  out_buffer = io.BytesIO()
  image.save(out_buffer, format='WEBP')
  return out_buffer.getvalue()

st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()
st.title("Image to WEBP Converter")

uploaded_files = st.file_uploader("Choose multiple images to convert:", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files is not None:
  for uploaded_file in uploaded_files:
    # Read the uploaded image data
    image_data = uploaded_file.read()

    # Convert the image to WEBP format
    webp_data = convert_to_webp(image_data)

    # Display the original image with caption
    st.subheader(f"Original Image: {uploaded_file.name}")
    st.image(image_data)

    # Download button for the converted WEBP image (modified)
    st.subheader(f"Converted WEBP Image: {uploaded_file.name}.webp")
    st.download_button(label="Download WEBP", data=webp_data, file_name=f"{uploaded_file.name}.webp")

