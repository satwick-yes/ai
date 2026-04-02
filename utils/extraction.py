import PyPDF2
import docx
import os

def extract_text_from_pdf(file_stream):
    """
    Extract text from a PDF file stream.
    """
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_text_from_docx(file_stream):
    """
    Extract text from a DOCX file stream.
    """
    try:
        doc = docx.Document(file_stream)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def get_text_from_file(file_name, file_content):
    """
    Determine file type and extract text.
    """
    from io import BytesIO
    file_stream = BytesIO(file_content)
    
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(file_stream)
    elif file_name.endswith('.docx'):
        return extract_text_from_docx(file_stream)
    else:
        return ""
