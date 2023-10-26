import streamlit as st
import logging
import LLM

# This file mostly covers UI via streamlit and functions involving displayed output
# Keep all management of the LLM model in the LLM.py file

# debug configration
level = logging.DEBUG  # sets level of shown logs
fmt = "[%(levelname)s] %(asctime)s - %(message)s"  # log output
logging.basicConfig(level=level, format=fmt)  # configure module

# session state initialisers
if "history" not in st.session_state:
    st.session_state.history = [{"user": "ai", "body": "Hello, I am the AI, please ask me a question!"}]
if "loaded_model" not in st.session_state:
    st.session_state.model = LLM.PdfQuestioner()

# Streamlit Main UI
st.set_page_config(page_title="PDF Questioner", page_icon="📚", layout="wide")
st.title(body="PDF Questioner")
st.write("Please load a PDF or saved vector before asking questions")
st.warning("Intial loading may take a while, as it has to download the model")

# PDF Sidebar
with st.sidebar:
    st.title("Data Management")
    st.subheader("Loading PDF")
    pdf_file = st.file_uploader(label="Upload PDF", type="pdf")
    if st.button(label="Submit PDF", key="UploadPDF"):
        pass

    st.subheader("Load Saved Vectors")
    st.write("This is where the Vectors dialog will go")

# Main Body
chat = st.container()
if st.session_state.model.loaded:
    for message in st.session_state.history:
        with st.chat_message(name=message["user"]):
            st.write(message["body"])

    if prompt := st.chat_input("", key="question"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.history.append({"user": "user", "body": prompt})
