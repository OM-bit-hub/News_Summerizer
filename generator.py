import os
import cohere
from transformers import T5Tokenizer, T5ForConditionalGeneration
from deep_translator import GoogleTranslator


class DualGenerator:
    LANGS = {"English": "en", "Hindi": "hi", "Marathi": "mr"}

    def __init__(self, config_path=None):
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("Cohere API key not found in environment variables")
        self.cohere_client = cohere.Client(api_key)

        model = "T5_Fine_Tunned/t5-news-final"
        self.t5_tokenizer = T5Tokenizer.from_pretrained(model)
        self.t5_model = T5ForConditionalGeneration.from_pretrained(model)

    def prepare_prompt(self, user_query: str, context_docs: list[str], target_language: str = "English", max_docs: int = 5) -> str:
        context = "\n".join(context_docs[:max_docs]) if context_docs else ""
        return f"Summarize in {target_language}:\nUser Query: {user_query}\nContext:\n{context}"

    def generate_with_cohere(self, prompt: str) -> str:
        try:
            r = self.cohere_client.generate(
                prompt=prompt, 
                max_tokens=300, 
                temperature=0.3)
            return r.generations[0].text.strip()
        except:
            return ""

    def generate_with_t5(self, prompt: str) -> str:
        try:
            ids = self.t5_tokenizer.encode(
                "summarize: " + prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512)
            out = self.t5_model.generate(
                ids, 
                max_length=300, 
                min_length=50, 
                num_beams=4)
            return self.t5_tokenizer.decode(out[0], skip_special_tokens=True)
        except:
            return ""

    def translate_text(self, text: str, target_lang: str) -> str:
        if target_lang.lower() == "english" or not text:
            return text
        target_code = self.lang_code(target_lang)
        t = GoogleTranslator(source='en', target=target_code).translate(text)
        # Fix for Marathi-Hindi mismatch
        if target_code == "mr" and any(w in t for w in ["है", "था", "और", "इस", "के", "में"]):
            t = GoogleTranslator(source='en', target='mr').translate(text)
        return t

    def lang_code(self, lang_name: str) -> str:
        return self.LANGS.get(lang_name, "en")

    def needs_translation(self, text: str) -> bool:
        return not text or sum(c.isascii() for c in text) / len(text) > 0.8

    def generate_summaries(self, user_query: str, context_docs: list[str], target_language: str = "English") -> dict:
        # English version for evaluation
        eng_prompt = self.prepare_prompt(user_query, context_docs, "English")
        english_summaries = {
            "cohere": self.generate_with_cohere(eng_prompt),
            "t5": self.generate_with_t5(eng_prompt)
        }

        if target_language.lower() == "english":
            return {"english": english_summaries, "final": english_summaries}

        # target language generation
        tgt_prompt = self.prepare_prompt(user_query, context_docs, target_language)
        cohere_summary = self.generate_with_cohere(tgt_prompt)
        t5_summary = self.generate_with_t5(tgt_prompt)

        if self.needs_translation(cohere_summary):
            cohere_summary = self.translate_text(english_summaries["cohere"], target_language)
        if self.needs_translation(t5_summary):
            t5_summary = self.translate_text(english_summaries["t5"], target_language)

        return {
            "english": english_summaries, 
            "final": {"cohere": cohere_summary, "t5": t5_summary}
            }
