## This is the code for the LLM model itself.
## all GUI code should be managed in app.py
## The model is a class that can then be used within via app.py

# Imports
import logging
from PyPDF2 import PdfReader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.gpt4all import GPT4AllEmbeddings
from langchain.text_splitter import CharacterTextSplitter


# debug configration
LEVEL = logging.DEBUG  # sets level of shown logs
FMT = "[%(levelname)s] %(asctime)s - %(message)s"  # log output
logging.basicConfig(level=LEVEL, format=FMT)  # configure module


# takes a list of pdf files and returns a list of pages
def __load_pdf(files):
    # logging.debug(f"Loading PDF: {files}")
    pages = []
    for pdf in files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            pages.append(page.extract_text())
    # logging.debug(f"Loaded PDF: {pages[0]}")
    return pages


# Chunks text into 400 character chunks with 100 character overlap
def __chunk_text(text):
    # takes a string and returns a list of strings
    # logging.debug(f"Chunking text: {text}")
    splitter = CharacterTextSplitter(separator="\n", chunk_size=400, chunk_overlap=100)
    docs = splitter.create_documents(text)
    chunks = splitter.split_documents(docs)
    return chunks


# places chunks into vector db
def __vectorise_chunks(chunks):
    # logging.debug(f"Vectorising chunks: {chunks[0]}")
    embedding = GPT4AllEmbeddings(model_name="mistral-7b-instruct-v0.1.Q4_0.gguf", client=None)  # type: ignore
    vector = FAISS.from_documents(chunks, embedding=embedding)
    return vector


# main processing function to call
def process_pdf(files):
    pages = __load_pdf(files)
    chunks = __chunk_text(pages)
    vector = __vectorise_chunks(chunks)
    return vector
