import PIL
import streamlit as st
from PIL import Image
import io


st.set_page_config(
    page_title="Resize Images",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.page_link("Home.py", label="H O M E", icon="🏡")
st.divider()
def resize_image(image, width, height, resample_filter=PIL.Image.LANCZOS):

    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    if width / height > aspect_ratio:
        new_height = int(width / aspect_ratio)
        new_width = width
    else:
        new_width = int(height * aspect_ratio)
        new_height = height

    resized_image = image.resize((new_width, new_height), resample=resample_filter)
    return resized_image

def main():
    st.title("Image Resizer")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption="Original Image")

        width = st.number_input("Width", min_value=1, value=300)
        height = st.number_input("Height", min_value=1, value=300)

        if st.button("Resize"):
            resized_image = resize_image(image, width, height)
            st.image(resized_image, caption="Resized Image")

            # Convert to RGB if necessary
            if resized_image.mode == "RGBA":
                resized_image = resized_image.convert("RGB")

            # Create a BytesIO buffer to store the resized image data
            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format="JPEG", quality=95)  # Adjust quality as needed

            # Download button
            st.download_button(
                label="Download Resized Image",
                data=img_bytes.getvalue(),
                file_name="resized_image.jpg",
                mime="image/jpeg"
            )

            # Explicitly resize without maintaining aspect ratio
            resized_image = resized_image.resize((width, height), resample=PIL.Image.NEAREST)

            # Create a BytesIO buffer for the explicitly resized image
            explicit_img_bytes = io.BytesIO()
            resized_image.save(explicit_img_bytes, format="JPEG", quality=95)  # Adjust quality as needed

            # Download button for explicitly resized image
            st.download_button(
                label="Download Resized Image (No Aspect Ratio)",
                data=explicit_img_bytes.getvalue(),
                file_name="resized_image_no_aspect_ratio.jpg",
                mime="image/jpeg"
            )

if __name__ == "__main__":
    main()