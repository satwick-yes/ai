import traceback
import sys
import os

# Add backend to path to import utils
sys.path.append(os.path.abspath('backend'))

try:
    import easyocr
    print(f"EasyOCR Version: {easyocr.__version__}")
    print("Attempting to initialize easyocr.Reader(['en'], gpu=False)...")
    reader = easyocr.Reader(['en'], gpu=False)
    print("Initialization successful!")
except Exception as e:
    print("Initialization FAILED with the following error:")
    traceback.print_exc()
