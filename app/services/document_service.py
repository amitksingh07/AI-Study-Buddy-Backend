from pypdf import PdfReader
from docx import Document
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"\n--- Page {page_num + 1} ---\n{page_text.strip()}"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text
