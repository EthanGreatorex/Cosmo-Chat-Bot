import streamlit as st
from pathlib import Path
from pdf_to_text import convert_pdf_to_txt

st.set_page_config(
    layout="wide",
)
@st.cache_data
def get_pdf_text(file):
    return convert_pdf_to_txt(file)

st.image(image='images/cosmo.png', width=150)
st.info("Hello again! Here you can upload a file for my to analyse! 📄")
file_upload = st.file_uploader("Upload your file:", type=['pdf', 'csv', 'txt'])

if file_upload:
    with st.spinner("Processing..."):
        file_extension = Path(file_upload.name).suffix
        if file_extension == '.pdf':
            AI_CONTEXT = get_pdf_text(file_upload)
            st.success("PDF content extracted!")

            st.session_state["AI_CONTEXT"] = AI_CONTEXT
            st.write("Context saved! You can now navigate to 'Chat with Cosmo'.")
        elif file_extension in ['.txt', '.csv']:
            AI_CONTEXT = file_upload.read().decode('utf-8')
            st.success("File content loaded!")
            st.session_state["AI_CONTEXT"] = AI_CONTEXT
            st.write("Context saved! You can now navigate to 'Chat with Cosmo'.")
            
        else:
            st.error("Unsupported file format.")
