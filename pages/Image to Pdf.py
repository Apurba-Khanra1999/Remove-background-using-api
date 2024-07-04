import streamlit as st
from PIL import Image
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass


def convert_images_to_pdf(image_files):
    pdf = PDF()
    for image_file in image_files:
        img = Image.open(image_file)
        pdf.add_page(format=(img.width, img.height))
        pdf.image(image_file, x=0, y=0, w=img.width, h=img.height)
    return pdf


def main():
    st.title("Image to PDF Converter")
    st.write("Upload images to convert them into a single PDF file.")

    uploaded_files = st.file_uploader("Choose image files", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

    if uploaded_files:
        images = []
        for file in uploaded_files:
            image = Image.open(file)
            image_path = f"temp_{file.name}"
            image.save(image_path)
            images.append(image_path)

        if st.button("Convert to PDF"):
            pdf = convert_images_to_pdf(images)
            pdf_output = "output.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as pdf_file:
                st.download_button(label="Download PDF", data=pdf_file, file_name="output.pdf")


if __name__ == "__main__":
    main()
