import requests
import streamlit as st
from PIL import Image, ImageDraw
from io import BytesIO
from datetime import datetime

# Define your Remove.bg API key
API_KEY = 'NAJbdpgiji8hrV9gTw1oH99g'


# Function to create a linear gradient background
def create_gradient_bg(size, color1, color2):
    width, height = size
    base = Image.new('RGBA', (width, height), color1)
    top = Image.new('RGBA', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []

    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)

    base.paste(top, (0, 0), mask)
    return base


# Page Configurations
st.set_page_config(
    page_title="Tool Box - Background Remover",
    page_icon="🖼️",
    layout="wide",
)

# Add custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header { text-align: center; font-size: 36px; color: #2E86C1; font-weight: bold; }
    .subheader { text-align: center; font-size: 20px; color: #333333; margin-top: -15px; }
    .centered-text { text-align: center; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px 24px; font-size: 16px; }
    .stButton>button:hover { background-color: #45a049; }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">Background Remover Tool</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Easily remove image backgrounds and add solid or gradient color backgrounds.</p>',
            unsafe_allow_html=True)
st.divider()

# Image Upload or Path Input Section
upload_or_path = st.radio("Choose Image Source", ("Upload Image", "Enter Image Path"))

if upload_or_path == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Get original filename without extension
        original_filename = uploaded_file.name.split('.')[0]

        # Show progress while making API request
        with st.spinner('Removing background...'):
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': uploaded_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )

        if response.status_code == requests.codes.ok:
            st.success("Background removed successfully!")
            processed_image = Image.open(BytesIO(response.content))

            # Display original and processed images side by side
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_file, caption="Original Image", use_column_width=True)
            with col2:
                st.image(processed_image, caption="Image Without Background", use_column_width=True)

            # Option to add solid or gradient background color
            st.markdown('<div class="centered-text"><h2>Add a background:</h2></div>', unsafe_allow_html=True)
            bg_option = st.radio("Choose Background Type", ["None", "Solid Color", "Gradient"], key="bg_option")

            if bg_option == "Solid Color":
                bg_color = st.color_picker("Pick a background color", "#ffffff", key="color_picker")
                bg_color_rgb = Image.new("RGBA", processed_image.size, bg_color)

                final_image = Image.alpha_composite(bg_color_rgb, processed_image)
                st.image(final_image, caption="Image with Solid Color Background", use_column_width=True)

            elif bg_option == "Gradient":
                color1 = st.color_picker("Pick first gradient color", "#ff0000", key="color1")
                color2 = st.color_picker("Pick second gradient color", "#0000ff", key="color2")

                gradient_bg = create_gradient_bg(processed_image.size, color1, color2)
                final_image = Image.alpha_composite(gradient_bg, processed_image)
                st.image(final_image, caption="Image with Gradient Background", use_column_width=True)
            else:
                final_image = processed_image

            # Download button with timestamp and original filename
            img_bytes = BytesIO()
            final_image.save(img_bytes, format="PNG")
            current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{original_filename}_{current_timestamp}.png"
            st.download_button(
                label="Download Processed Image",
                data=img_bytes.getvalue(),
                file_name=file_name,
                mime='image/png'
            )
        else:
            st.error(f"Error: {response.status_code}, {response.text}")

elif upload_or_path == "Enter Image Path":
    image_path = st.text_input("Enter the image URL")

    if image_path:
        # Show progress while making API request
        with st.spinner('Removing background...'):
            try:
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    data={'image_url': image_path, 'size': 'auto'},
                    headers={'X-Api-Key': API_KEY},
                )

                if response.status_code == requests.codes.ok:
                    st.success("Background removed successfully!")
                    processed_image = Image.open(BytesIO(response.content))

                    # Display original and processed images side by side
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(image_path, caption="Original Image", use_column_width=True)
                    with col2:
                        st.image(processed_image, caption="Image Without Background", use_column_width=True)

                    # Option to add solid or gradient background color
                    st.markdown('<div class="centered-text"><h2>Add a background:</h2></div>', unsafe_allow_html=True)
                    bg_option = st.radio("Choose Background Type", ["None", "Solid Color", "Gradient"],
                                         key="bg_option_path")

                    if bg_option == "Solid Color":
                        bg_color = st.color_picker("Pick a background color", "#ffffff", key="color_picker_path")
                        bg_color_rgb = Image.new("RGBA", processed_image.size, bg_color)

                        final_image = Image.alpha_composite(bg_color_rgb, processed_image)
                        st.image(final_image, caption="Image with Solid Color Background", use_column_width=True)

                    elif bg_option == "Gradient":
                        leftgrad, rightgrad = st.columns(2)
                        with leftgrad:
                            color1 = st.color_picker("Pick first gradient color", "#ff0000", key="color1_path")
                        with rightgrad:
                            color2 = st.color_picker("Pick second gradient color", "#0000ff", key="color2_path")

                        gradient_bg = create_gradient_bg(processed_image.size, color1, color2)
                        final_image = Image.alpha_composite(gradient_bg, processed_image)
                        st.image(final_image, caption="Image with Gradient Background", use_column_width=True)
                    else:
                        final_image = processed_image

                    # Download button with timestamp and original filename
                    img_bytes = BytesIO()
                    final_image.save(img_bytes, format="PNG")
                    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = f"image_{current_timestamp}.png"
                    st.download_button(
                        label="Download Processed Image",
                        data=img_bytes.getvalue(),
                        file_name=file_name,
                        mime='image/png'
                    )
                else:
                    st.error(f"Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"Error processing image: {e}")
