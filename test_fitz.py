import fitz
import sys
import os
from io import BytesIO

# Try opening a PDF if one exists
pdf_path = None
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            break
    if pdf_path: break

if pdf_path:
    print(f"Testing with PDF: {pdf_path}")
    try:
        doc = fitz.open(pdf_path)
        print(f"Pages: {len(doc)}")
        page = doc[0]
        pix = page.get_pixmap()
        print(f"Pixmap size: {pix.width}x{pix.height}")
        img_bytes = pix.tobytes("png")
        print(f"Image bytes size: {len(img_bytes)}")
        print("Fitz rendering successful!")
    except Exception as e:
        print(f"Fitz failed: {e}")
else:
    print("No PDF found to test with.")
