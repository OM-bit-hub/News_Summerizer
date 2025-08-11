# 🧠 RAG-Based News Summarizer
## Project by -
## 1. Om Dhengle
## 2. Ritesh Taru - https://github.com/Riteshtaru343/RAG_Based_News_Summerizer.git

This project is a modular, multilingual news summarization app powered by:
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Cohere LLM
- ✅ ChromaDB (for persistent memory)
- ✅ Multi-format input (Text, URL, PDF, Image)
- ✅ gTTS voice response
- ✅ Streamlit UI

---

## 📦 Features

- 🔍 Input via text, URL, PDF, or image (OCR)
- 🌐 Multilingual summaries (English, Hindi, Marathi)
- 🧠 Memory-based response with ChromaDB vector store
- 🗣️ Voice playback using gTTS
- 📌 Automatically stores and reuses inputs for future queries

---

## 🚀 How to Run

### 1. Clone the Repo & Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Install System Dependencies
#### Tesseract (for OCR from images)
- **Ubuntu/Debian**: `sudo apt install tesseract-ocr`
- **Windows**: [Download Tesseract](https://github.com/tesseract-ocr/tesseract/wiki)

---

### 3. Set up API Keys
Replace or add your Cohere API key:

- Option 1 (dev): Replace in `summarization.py`
```python
co = cohere.Client("<your-api-key>")
```

- Option 2 (prod): Use Streamlit secrets
Create `.streamlit/secrets.toml`:
```toml
COHERE_API_KEY = "your-key-here"
```

---

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🧪 Example Inputs
- 📝 Text: Paste article text directly
- 🌐 URL: Paste a news article link
- 📄 PDF: Upload a news PDF
- 🖼️ Image: Upload a screenshot of a news article

---

## 📂 Folder Structure

```
├── app.py                  # Streamlit UI
├── extractor.py            # Handles input from PDF, URL, images
├── retrieval.py            # Vector DB (Chroma) logic
├── summarization.py        # Summarization and translation
├── rag_pipeline.py         # Core logic combining everything
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
```

---

## 🌱 Future Ideas

- [ ] Feedback & rating for summary
- [ ] Memory browser (see past queries/summaries)
- [ ] Clustering or topic classification (e.g., politics, sports, tech)

---


