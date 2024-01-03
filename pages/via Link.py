import requests
import streamlit as st

uploaded_file = st.text_input("Provide the path of the image")

if uploaded_file:
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        data={
            'image_url': uploaded_file,
            'size': 'auto'
        },
        headers={'X-Api-Key': 'NAJbdpgiji8hrV9gTw1oH99g'},
    )

    if response.status_code == requests.codes.ok:
        original_col, converted_col = st.columns(2)


        with original_col:
            st.subheader("Original Image")
            st.image(uploaded_file, use_column_width=True)

        with converted_col:
            st.subheader("Converted Image")
            st.image(response.content, use_column_width=True)

        with st.expander("Click to download"):
            st.download_button(
                label="Download Converted Image",
                data=response.content,
                file_name='../no-bg.png',
                mime='image/png',
            )
    elif response.status_code == 400 and "No image given" in response.text:
        st.warning("Please provide a valid image path.")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
else:
    st.warning("Please provide the path of the image.")
