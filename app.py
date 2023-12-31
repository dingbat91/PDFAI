import streamlit as st
import logging
from utils import process_pdf
from langchain.llms.gpt4all import GPT4All
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, PromptTemplate

# This file mostly covers UI via streamlit and functions involving displayed output
# Keep all management of the LLM model in the LLM.py file

# page config
st.set_page_config(page_title="PDF Questioner", page_icon="📚", layout="wide")

# debug configration
LEVEL = logging.DEBUG  # sets level of shown logs
FMT = "[%(levelname)s] %(asctime)s - %(message)s"  # log output
logging.basicConfig(level=LEVEL, format=FMT)  # configure module

# template initiation
TEMPLATE = """
You have been given a rulebook for a TTRPG
answer the following questions about the rulebook using the context provided. Try to give certain answers and avoid being vague. 
Do not make up rules or answers, if the context does not provide the answer say you don't know.

The question is: {question}
The context is: {context}

output you answer in a human readable format. Don't tab or indent your answer.

"""


# Loads the model and stores the result in a cache
@st.cache_resource
def load_model():
    return GPT4All(model="mistral-7b-openorca.Q4_0.gguf", max_tokens=1000, streaming=True)  # type: ignore


# session state initialisers
if "history" not in st.session_state:
    st.session_state.history = [{"user": "ai", "body": "Hello, I am the AI, please ask me a question!"}]
if "vector" not in st.session_state:
    st.session_state.vector = None
if "model" not in st.session_state:
    st.session_state.model = load_model()

# Streamlit Main UI
st.title(body="PDF Questioner")
st.markdown("Please load a PDF or saved vector before asking questions")
st.warning("Intial loading may take a while, as it has to download the model")

# PDF Sidebar
with st.sidebar:
    st.title("Data Management")
    st.subheader("Loading PDF")
    pdf_file = st.file_uploader(label="Upload PDF", type="pdf", accept_multiple_files=True)
    if st.button(label="Submit PDF", key="UploadPDF"):
        logging.debug(pdf_file)
        with st.spinner(text="Loading PDFs"):
            st.session_state.vector = process_pdf(pdf_file)
        logging.debug(f"Vector loaded from PDF: {st.session_state.vector}")

    st.subheader("Load Saved Vectors")
    st.markdown("This is where the Vectors dialog will go")

# Main Body
chat = st.container()
for message in st.session_state.history:
    with st.chat_message(name=message["user"]):
        st.markdown(message["body"])

if prompt := st.chat_input("", key="question"):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.history.append({"user": "user", "body": prompt})  # type: ignore

    if st.session_state.vector is None:
        st.error("Please load a PDF or saved vector before asking questions")
        st.stop()

    chain = (
        {"question": RunnablePassthrough(), "context": st.session_state.vector.as_retriever(search_kwargs={"k": 5, "fetch_k": 20, "score_threshold": 3})}  # type: ignore
        | PromptTemplate.from_template(TEMPLATE)
        | st.session_state.model
    )
    # with st.spinner(text="Generating Answer"):
    with st.chat_message("ai"):
        with st.spinner(text="Generating Answer"):
            message = chain.invoke(prompt)
            st.markdown(message)
    st.session_state.history.append({"user": "ai", "body": message})
