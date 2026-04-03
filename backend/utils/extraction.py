import docx
import os
import pdfplumber
import numpy as np
from io import BytesIO

# OCR Singleton Loader
_easyocr_reader = None

def get_ocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            print("🚀 OCR: Initializing EasyOCR Reader (English)...")
            # This may take a minute if models need to be downloaded
            _easyocr_reader = easyocr.Reader(['en'], gpu=False, download_enabled=True)
            print("✅ OCR: EasyOCR initialized and ready.")
        except Exception as e:
            print(f"❌ OCR: Failed to initialize EasyOCR: {e}")
    return _easyocr_reader

def extract_text_from_pdf(file_stream):
    """
    Extract text using pdfplumber, with OCR fallback if no text found.
    """
    try:
        text = ""
        # Store stream position to reset for OCR if needed
        file_stream.seek(0)
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        
        # If no text found or it's very short, try OCR fallback
        clean_text = text.strip()
        if not clean_text or len(clean_text) < 20:
            print(f"🔍 OCR: No text found in PDF (Length: {len(clean_text)}). Falling back to OCR...")
            file_stream.seek(0)
            return extract_text_from_pdf_ocr(file_stream)
            
        print(f"📄 OCR: Successfully extracted {len(clean_text)} chars using pdfplumber.")
        return text
    except Exception as e:
        print(f"⚠️ OCR: Error during standard PDF extraction, trying OCR: {e}")
        file_stream.seek(0)
        return extract_text_from_pdf_ocr(file_stream)

def extract_text_from_pdf_ocr(file_stream):
    """
    Render PDF pages to images and run OCR using EasyOCR.
    """
    try:
        import fitz  # PyMuPDF
        reader = get_ocr_reader()
        if not reader:
            print("❌ OCR: Reader not available.")
            return ""
            
        text = ""
        pdf_doc = fitz.open(stream=file_stream, filetype="pdf")
        
        # Limit to first 5 pages for screening
        num_pages = min(len(pdf_doc), 5)
        print(f"📷 OCR: Rendering and scanning {num_pages} pages...")
        
        for page_num in range(num_pages):
            page = pdf_doc.load_page(page_num)
            # Increase zoom for better OCR accuracy (2x)
            matrix = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=matrix) 
            img_bytes = pix.tobytes("png")
            
            # EasyOCR scan
            results = reader.readtext(img_bytes)
            page_text = " ".join([res[1] for res in results])
            text += page_text + "\n"
            print(f"✅ OCR: Page {page_num+1}/{num_pages} processed.")
            
        return text
    except Exception as e:
        print(f"Error during PDF OCR: {e}")
        return ""

def extract_text_from_image(file_content):
    """
    Run OCR on image bytes (JPG, PNG).
    """
    try:
        reader = get_ocr_reader()
        if not reader:
            return ""
        results = reader.readtext(file_content)
        return " ".join([res[1] for res in results])
    except Exception as e:
        print(f"Error during Image OCR: {e}")
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
    Determine file type and extract text, with image/OCR support.
    """
    file_stream = BytesIO(file_content)
    file_name_lower = file_name.lower()
    
    if file_name_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_stream)
    elif file_name_lower.endswith('.docx'):
        return extract_text_from_docx(file_stream)
    elif file_name_lower.endswith(('.png', '.jpg', '.jpeg')):
        print(f"Processing image file: {file_name}")
        return extract_text_from_image(file_content)
    else:
        return ""
