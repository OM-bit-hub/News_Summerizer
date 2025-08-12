# extractor.py

import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import fitz  
import io

def extract_text_from_text(text: str) -> str:
    return text.strip()

def extract_text_from_url(url: str) -> str:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return "\n".join(p.get_text() for p in paragraphs if p.get_text().strip())
    except Exception as e:
        return f"[Error extracting from URL]: {e}"

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        return f"[Error extracting from PDF]: {e}"

def extract_text_from_image(file_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(file_bytes)).convert('RGB')
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[Error extracting from Image]: {e}"
