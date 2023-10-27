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
level = logging.DEBUG  # sets level of shown logs
fmt = "[%(levelname)s] %(asctime)s - %(message)s"  # log output
logging.basicConfig(level=level, format=fmt)  # configure module


def __load_pdf(files):
    # takes a list of pdf files and returns a list of pages
    # logging.debug(f"Loading PDF: {files}")
    pages = []
    for pdf in files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            pages.append(page.extract_text())
    # logging.debug(f"Loaded PDF: {pages[0]}")
    return pages


def __chunk_text(text):
    # takes a string and returns a list of strings
    # logging.debug(f"Chunking text: {text}")
    splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents(text)
    return chunks


def __vectorise_chunks(chunks):
    # logging.debug(f"Vectorising chunks: {chunks[0]}")
    embedding = GPT4AllEmbeddings(model_name="mistral-7b-instruct-v0.1.Q4_0.gguf", client=None)  # type: ignore
    vector = FAISS.from_documents(chunks, embedding=embedding)
    return vector


def process_pdf(files):
    pages = __load_pdf(files)
    chunks = __chunk_text(pages)
    vector = __vectorise_chunks(chunks)
    return vector
