from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from newspaper import Article
import tempfile

def extract_text_from_text(text):
    return text.strip()

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        return f"[Error extracting from URL]: {e}"

def extract_text_from_pdf(uploaded_file):
    try:
        uploaded_file.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file.flush()
            doc = fitz.open(tmp_file.name)
            text = "\n".join(page.get_text() for page in doc)
        return text.strip()
    except Exception as e:
        return f"[Error extracting from PDF]: {e}"

def extract_text_from_image(uploaded_file):
    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image, config="--psm 6").strip()
    except Exception as e:
        return f"[Error extracting from image]: {e}"
