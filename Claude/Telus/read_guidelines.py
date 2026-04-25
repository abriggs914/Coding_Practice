import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# If on Windows, set this path (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to your PDF
pdf_path = r"D:\Important documents\Telus\general rating guidelines condensed.pdf"

# Convert PDF to images
images = convert_from_path(pdf_path, dpi=300)

full_text = []

for i, image in enumerate(images):
    print(f"Processing page {i + 1}...")
    
    # Optional: convert to grayscale for better OCR
    gray = image.convert("L")
    
    # OCR
    text = pytesseract.image_to_string(gray)
    full_text.append(text)

# Combine all pages
result = "\n\n".join(full_text)

print("\n=== OCR OUTPUT ===\n")
print(result)