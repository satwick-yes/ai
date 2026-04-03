import os
import sys
from io import BytesIO

# Add backend to path to import utils
sys.path.append(os.path.abspath('backend'))

try:
    from backend.utils.extraction import get_ocr_reader, get_text_from_file
    print("Imports successful")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# Try initializing OCR reader
print("Test: Initializing OCR reader...")
reader = get_ocr_reader()
if reader:
    print("EasyOCR reader initialized successfully")
else:
    print("EasyOCR reader initialization FAILED")

# Create a small dummy PDF or just use one for a quick test if one exists
# Actually let's just try to check if easyocr is reachable
try:
    import easyocr
    print(f"EasyOCR version: {easyocr.__version__}")
except ImportError:
    print("EasyOCR is NOT installed in this environment")

try:
    import fitz
    print(f"PyMuPDF (fitz) version: {fitz.version}")
except ImportError:
    print("PyMuPDF (fitz) is NOT installed in this environment")
