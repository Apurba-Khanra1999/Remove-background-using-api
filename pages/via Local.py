import requests
import streamlit as st
import os

# Define your Remove.bg API key
API_KEY = 'NAJbdpgiji8hrV9gTw1oH99g'

# Display Streamlit widget to upload an image
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

        # Save the processed image
        with st.expander("Click to download"):
            st.image(response.content, caption="Processed Image", use_column_width=True)
            st.download_button(
                label="Download Processed Image",
                data=response.content,
                file_name='../no-bg.png',
                mime='image/png',
            )
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
else:
    st.info("Please upload an image.")
