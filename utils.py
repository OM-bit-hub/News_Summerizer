import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import tempfile

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return '\n'.join(p.text for p in paragraphs if p.text.strip())
    except Exception as e:
        return f"Error reading URL: {e}"

def extract_pdf_text(file):
    try:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in pdf])
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_image_text(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        image = Image.open(tmp_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error reading image: {e}"
