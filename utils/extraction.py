import io
import PyPDF2
from docx import Document
import logging

def extract_text_from_pdf(file_content):
    """
    Extracts text from a PDF file byte stream.
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        logging.error(f"Error extracting PDF: {e}")
    return text

def extract_text_from_docx(file_content):
    """
    Extracts text from a DOCX file byte stream.
    """
    text = ""
    try:
        doc = Document(io.BytesIO(file_content))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        logging.error(f"Error extracting DOCX: {e}")
    return text

def extract_text(file_name, file_content):
    """
    Router for text extraction based on file extension.
    """
    if file_name.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif file_name.lower().endswith('.docx'):
        return extract_text_from_docx(file_content)
    else:
        # Assume plain text for other types
        try:
            return file_content.decode('utf-8')
        except:
            return ""
