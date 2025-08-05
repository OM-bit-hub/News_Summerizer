import cohere
from deep_translator import GoogleTranslator
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])

SUMMARY_PROMPT_TEMPLATE = """You are a helpful assistant. SUMMARIZE the following news article based on the provided context and query BY generating an abstractive summary with the help of relevant documents.

Context:
{context}

Query:
{query}

Answer:"""

def generate_abstractive_summary(context, query):
    prompt = SUMMARY_PROMPT_TEMPLATE.format(context=context, query=query)
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=500,
            temperature=0.3
        )
        if not response.generations:
            return "[Error]: Empty response from Cohere"
        return response.generations[0].text.strip()
    except Exception as e:
        return f"[Error generating summary]: {e}"

def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        return f"[Translation failed for {target_lang}]: {e}"
