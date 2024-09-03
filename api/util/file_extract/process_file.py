from api.util.utils import clean_text
import pymupdf

def pdf_to_text(file): # Transforms PDF(an InMemoryUploadedFile object) to text using PyMuPDF
    with file.open("rb") as file:
        doc = pymupdf.Document(stream=file.read())
        text = ""
        for page in doc:
            text += page.get_text()
    return clean_text(text)
