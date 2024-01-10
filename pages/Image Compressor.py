import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io
import requests

st.set_page_config(
    page_title="Remove AI",
    page_icon="🤖",
    layout="wide",
)

st.title("Image Compressor")

# Option for image upload or URL input
upload_or_url = st.radio("Choose how to provide the image:", ("Upload", "Enter URL"))

if upload_or_url == "Upload":
    # Handle image upload (existing logic)
    uploaded_file = st.file_uploader("Choose an image to compress", type=["jpg", "jpeg", "png"])
    # ... (rest of the code for image upload)

else:
    # Handle image URL input
    image_url = st.text_input("Enter image URL")

    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Raise an exception for error status codes

            # Open the image from the response stream
            image = Image.open(response.raw)

            # Display the original image
            st.image(image, caption="Original Image", use_column_width=True)

            # Compress the image (same logic as before)
            quality = st.slider("Compression Quality", min_value=1, max_value=95, value=75, step=1)
            compressed_image = io.BytesIO()
            image.save(compressed_image, format="JPEG", quality=quality)

            # Download the compressed image
            st.download_button(
                label="Download Compressed Image",
                data=compressed_image.getvalue(),
                file_name=f"compressed_{image_url.split('/')[-1]}",  # Use filename from URL
                mime="image/jpeg"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching image from URL: {e}")
        except Exception as e:
            st.error(f"Error processing image: {e}")