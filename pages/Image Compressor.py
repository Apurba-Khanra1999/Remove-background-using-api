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

# List to keep track of processed images for grid display and conditional zip creation
processed_images = []
fixed_height = 300  # Set a fixed height for all images

if upload_or_url == "Upload":
    # Handle multiple image uploads
    uploaded_files = st.file_uploader("Choose images to compress", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        quality = st.slider("Compression Quality", min_value=1, max_value=95, value=50, step=1)

        for uploaded_file in uploaded_files:
            try:
                image = Image.open(uploaded_file)

                # Convert RGBA image to RGB
                if image.mode == 'RGBA':
                    image = image.convert('RGB')

                # Resize the image to a fixed height while maintaining aspect ratio
                aspect_ratio = image.width / image.height
                new_width = int(fixed_height * aspect_ratio)
                image.thumbnail((new_width, fixed_height))

                # Compress the image
                compressed_image = io.BytesIO()
                image.save(compressed_image, format="JPEG", quality=quality)
                compressed_image.seek(0)

                # Store the compressed image in the list for later use
                processed_images.append((uploaded_file.name, image, compressed_image))

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

                    # Resize the image to a fixed height while maintaining aspect ratio
                    aspect_ratio = image.width / image.height
                    new_width = int(fixed_height * aspect_ratio)
                    image.thumbnail((new_width, fixed_height))

                    # Compress the image
                    compressed_image = io.BytesIO()
                    image.save(compressed_image, format="JPEG", quality=quality)
                    compressed_image.seek(0)

                    # Store the compressed image in the list for later use
                    processed_images.append((url.split('/')[-1], image, compressed_image))

                    images_processed = True

                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching image from URL {url}: {e}")
                except Exception as e:
                    st.error(f"Error processing image from URL {url}: {e}")

# Display images in a grid layout (2 per row) with fixed height
if images_processed:
    cols = st.columns(2)  # Create two columns for grid layout
    for idx, (img_name, original_image, _) in enumerate(processed_images):
        col = cols[idx % 2]  # Alternates between the two columns
        col.image(original_image, caption=f"Original Image: {img_name}", use_column_width=True)

# Prepare the zip file for download if more than one image was processed
if images_processed:
    if len(processed_images) > 1:
        # Create a zip file only if there is more than one image
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for img_name, _, compressed_image in processed_images:
                # Add the compressed image to the zip file
                zip_file.writestr(f"compressed_{img_name}", compressed_image.read())

        zip_buffer.seek(0)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download All Compressed Images as Zip",
            data=zip_buffer,
            file_name=f"compressed_images_{current_time}.zip",
            mime="application/zip"
        )
    else:
        # If only one image, offer the individual compressed image for download
        img_name, _, compressed_image = processed_images[0]
        st.download_button(
            label=f"Download Compressed Image: {img_name}",
            data=compressed_image.getvalue(),
            file_name=f"compressed_{img_name}",
            mime="image/jpeg"
        )