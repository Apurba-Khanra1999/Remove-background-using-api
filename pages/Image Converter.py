import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="PNG ↔ JPG Converter", layout="centered")

st.title("🖼️ Image Converter")
st.write("Upload an image and choose the format to convert.")

uploaded_file = st.file_uploader("Upload Image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Choose conversion format
    convert_to = st.radio("Convert to:", ("PNG", "JPG"))

    if st.button("Convert"):
        img_format = "PNG" if convert_to == "PNG" else "JPEG"

        # Convert image
        img_bytes = io.BytesIO()
        image = image.convert("RGB")  # Ensure no transparency for JPG
        image.save(img_bytes, format=img_format)
        img_bytes.seek(0)

        # Download Button
        st.success(f"Converted to {convert_to} successfully!")
        st.download_button(
            label=f"Download {convert_to}",
            data=img_bytes,
            file_name=f"converted.{convert_to.lower()}",
            mime=f"image/{convert_to.lower()}"
        )
