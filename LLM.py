## This is the code for the LLM model itself.
## all GUI code should be managed in app.py
## The model is a class that can then be used within via app.py

# Imports
import logging

# debug configration
level = logging.DEBUG  # sets level of shown logs
fmt = "[%(levelname)s] %(asctime)s - %(message)s"  # log output
logging.basicConfig(level=level, format=fmt)  # configure module


# LLM Model
class PdfQuestioner:
    def __init__(self):
        self.model = None
        self.vector = None
        self.pdfs = []
        self.history = []
        self.loaded = False

    def __str__(self) -> str:
        return f"PDF Questioner Model: {self.model}"

    def load_model(self, pdf_docs):
        self.pdfs = pdf_docs
        self.__load_pdfs()

    def __load_pdfs(self):
        pass
