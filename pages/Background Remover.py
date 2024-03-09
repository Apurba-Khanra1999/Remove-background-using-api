import requests
import streamlit as st

# Define your Remove.bg API key
API_KEY = 'NAJbdpgiji8hrV9gTw1oH99g'

st.set_page_config(
    page_title="Background Remover",
    page_icon="",
    layout="wide",
)

st.title("Background Remover")

# Option for image upload or path input
upload_or_path = st.radio("Choose how to provide the image:", ("Upload", "Enter Path"))

if upload_or_path == "Upload":
    # Handle image upload
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Make API request to Remove.bg
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': uploaded_file},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code == requests.codes.ok:
            st.success("Background removed successfully!")

            # Display the processed image
            st.image(response.content, caption="Processed Image", use_column_width=True)

            # Download the processed image
            st.download_button(
                label="Download Processed Image",
                data=response.content,
                file_name='no-bg.png',
                mime='image/png',
            )
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
else:
    # Handle image path input
    image_path = st.text_input("Enter the path of the image")

    if image_path:
        try:
            # Make API request to Remove.bg
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                data={
                    'image_url': image_path,
                    'size': 'auto'
                },
                headers={'X-Api-Key': API_KEY},
            )

            if response.status_code == requests.codes.ok:
                st.success("Background removed successfully!")

                # Display the processed image
                st.image(response.content, caption="Processed Image", use_column_width=True)

                # Download the processed image
                st.download_button(
                    label="Download Processed Image",
                    data=response.content,
                    file_name='no-bg.png',
                    mime='image/png',
                )
            elif response.status_code == 400 and "No image given" in response.text:
                st.warning("Please provide a valid image path.")
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            st.error(f"Error processing image: {e}")
    else:
        st.warning("Please provide the path of the image.")
