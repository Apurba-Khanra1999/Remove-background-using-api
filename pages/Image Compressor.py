import streamlit as st
from PIL import Image
import io
import requests
import zipfile
from datetime import datetime

st.set_page_config(
    page_title="Compress Images",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()
st.title("Image Compressor")

# Option for image upload or URL input
upload_or_url = st.radio("Choose how to provide the image:", ("Upload", "Enter URL"))

# Prepare a buffer to store the zip file
zip_buffer = io.BytesIO()

# Flag to check if any image is processed
images_processed = False

# Create a zip file in memory
with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

    if upload_or_url == "Upload":
        # Handle multiple image uploads
        uploaded_files = st.file_uploader("Choose images to compress", type=["jpg", "jpeg", "png"],
                                          accept_multiple_files=True)

        if uploaded_files:
            quality = st.slider("Compression Quality", min_value=1, max_value=95, value=75, step=1)

            for uploaded_file in uploaded_files:
                try:
                    image = Image.open(uploaded_file)

                    # Convert RGBA image to RGB
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')

                    # Display the original image
                    st.image(image, caption=f"Original Image: {uploaded_file.name}", use_column_width=True)

                    # Compress the image
                    compressed_image = io.BytesIO()
                    image.save(compressed_image, format="JPEG", quality=quality)
                    compressed_image.seek(0)

                    # Add the compressed image to the zip file
                    zip_file.writestr(f"compressed_{uploaded_file.name}", compressed_image.read())

                    images_processed = True

                except Exception as e:
                    st.error(f"Error processing image {uploaded_file.name}: {e}")

    else:
        # Handle image URL input
        image_urls = st.text_area("Enter image URLs (one per line)", placeholder="paste the URLs of the images")

        if image_urls:
            urls = image_urls.split("\n")
            quality = st.slider("Compression Quality", min_value=1, max_value=95, value=75, step=1)

            for url in urls:
                url = url.strip()
                if url:
                    try:
                        response = requests.get(url, stream=True)
                        response.raise_for_status()  # Raise an exception for error status codes

                        # Open the image from the response stream
                        image = Image.open(response.raw)

                        # Convert RGBA image to RGB
                        if image.mode == 'RGBA':
                            image = image.convert('RGB')

                        # Display the original image
                        st.image(image, caption=f"Original Image: {url.split('/')[-1]}", use_column_width=True)

                        # Compress the image
                        compressed_image = io.BytesIO()
                        image.save(compressed_image, format="JPEG", quality=quality)
                        compressed_image.seek(0)

                        # Add the compressed image to the zip file
                        zip_file.writestr(f"compressed_{url.split('/')[-1]}", compressed_image.read())

                        images_processed = True

                    except requests.exceptions.RequestException as e:
                        st.error(f"Error fetching image from URL {url}: {e}")
                    except Exception as e:
                        st.error(f"Error processing image from URL {url}: {e}")

# Prepare the zip file for download if images were processed
if images_processed:
    zip_buffer.seek(0)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="Download All Compressed Images as Zip",
        data=zip_buffer,
        file_name=f"compressed_images_{current_time}.zip",
        mime="application/zip"
    )
