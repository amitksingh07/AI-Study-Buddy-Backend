import fitz
from docx import Document
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page_text = doc[page_num].get_text().strip()
        if page_text:
            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text
