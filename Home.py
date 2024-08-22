import streamlit as st
import subprocess
import sys

st.set_page_config(
    page_title="Tool Box",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.logo(icon_image="logo.png", image="logofull.png")
st.image('header.png')
st.title('Our Products')
st.write('')
col1, col2, col3, col4 =st.columns(4)
with col1:
    with st.container(border=True):
        left, right = st.columns([1,4])
        with left:
            st.image('background.png', width=30)
        with right:
            st.write('Remove background from any images')
        if st.button("Background Remover"):
            st.switch_page("pages/Background Remover.py")
with col2:
    with st.container(border=True):
        left, right = st.columns([1, 4])
        with left:
            st.image('compressor.png', width=30)
        with right:
            st.write('Compress image size using sliders')
        if st.button("Image Compressor"):
            st.switch_page("pages/Image Compressor.py")
with col3:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('zip.png',width=30)
        with right:
            st.write('Zip multiple extension files at once')
        if st.button("Zip Maker"):
            st.switch_page("pages/Zip Maker.py")
with col4:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('pdf.png',width=30)
        with right:
            st.write('Convert any images into PDFs')
        if st.button("Image to Pdf"):
            st.switch_page("pages/Image to Pdf.py")

col5, col6, col7, col8 =st.columns(4)
with col5:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('i2w.png',width=30)
        with right:
            st.write('Convert multiple images into WEBP')
        if st.button("Image to WEBP"):
            st.switch_page("pages/Image to WEBP.py")
with col6:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('i2w.png',width=30)
        with right:
            st.write('Convert multiple WEBPs into JPG')
        if st.button("WEBP to JPG"):
            st.switch_page("pages/WEBP to JPG.py")

with col7:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('doc.png',width=30)
        with right:
            st.write('Convert any PDF into Word file')
        if st.button("PDF to Word"):
            st.switch_page("pages/PDF to Word.py")

with col8:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('merge.png',width=30)
        with right:
            st.write('Merge multiple pdfs into one.')
        if st.button("Merge PDFs"):
            st.switch_page("pages/Merge PDFs.py")

col9, col10, col11, col12 =st.columns(4)
with col9:
    with st.container( border= True):
        left, right = st.columns([1, 4])
        with left:
            st.image('compresspdf.png',width=30)
        with right:
            st.write('Compress multiple pdfs into one.')
        if st.button("Compress PDFs"):
            st.switch_page("pages/Compress PDF.py")

st.divider()
# st.markdown('Feel free to suggest an edit 📝', unsafe_allow_html=True)
# st.markdown('📩 Contact me - apurbakhanra09@gmail.com', unsafe_allow_html=True)
st.image('footer.png')