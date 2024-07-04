import streamlit as st
from PIL import Image
import io

def convert_to_webp(image_data):
  """Converts an image in byte format to WEBP format.

  Args:
      image_data: The image data in byte format.

  Returns:
      A byte array containing the converted WEBP image data.
  """
  image = Image.open(io.BytesIO(image_data))
  out_buffer = io.BytesIO()
  image.save(out_buffer, format='WEBP')
  return out_buffer.getvalue()

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

