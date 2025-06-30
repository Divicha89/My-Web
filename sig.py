import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Set page configuration
st.set_page_config(page_title="Screenshot Text Extractor", layout="wide")

# Title and description
st.title("📷 Screenshot Text Extractor")
st.markdown("Upload a screenshot to extract text using OCR. Ensure the image is clear for best results.")

# File uploader
uploaded_file = st.file_uploader("Choose a screenshot...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_container_width=True)

    # Convert PIL image to OpenCV format
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Preprocess image
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Divija Cherukuri\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # Windows example

    # Perform OCR
    try:
        extracted_text = pytesseract.image_to_string(thresh, lang='eng')
        st.subheader("Extracted Text:")
        st.text_area("Text Output", extracted_text, height=300)
        
        # Download button for extracted text
        st.download_button(
            label="Download Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error during OCR: {str(e)}")
else:
    st.info("Please upload an image to start text extraction.")