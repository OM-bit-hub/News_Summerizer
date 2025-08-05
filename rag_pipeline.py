from retrieval import add_to_memory, search_memory
from deep_translator import GoogleTranslator
import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])
MAX_CONTEXT_CHARS = 3000

def generate_response(query_text, target_languages=['en'], n_results=5, source_type="text"):
    try:
        retrieved_docs = search_memory(query_text, n_results=n_results)
        context = "\n".join(retrieved_docs) if retrieved_docs else query_text
        if len(context) > MAX_CONTEXT_CHARS:
            context = context[:MAX_CONTEXT_CHARS]

        prompt = f"""You are a helpful assistant that summarizes news articles.

Context:
{context}

Query:
{query_text}

Summary:"""

        cohere_response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=500,
            temperature=0.3
        )

        if not cohere_response.generations:
            return {lang: "[Error]: Empty response from Cohere" for lang in target_languages}

        english_summary = cohere_response.generations[0].text.strip()

        responses = {'en': english_summary}
        for lang in target_languages:
            if lang != 'en':
                try:
                    responses[lang] = GoogleTranslator(source='en', target=lang).translate(english_summary)
                except Exception as e:
                    responses[lang] = f"[Translation failed for {lang}]: {e}"

        if not retrieved_docs:
            metadata = {"summary": english_summary[:200], "source": source_type}
            add_to_memory(text=query_text, source_type=source_type, metadata_extra=metadata)

        return responses

    except Exception as e:
        return {lang: f"[Error]: {e}" for lang in target_languages}
