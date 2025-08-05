import streamlit as st
from rag_pipeline import generate_response
from extractor import (
    extract_text_from_text,
    extract_text_from_url,
    extract_text_from_pdf,
    extract_text_from_image,
)
from gtts import gTTS
import io

st.set_page_config(page_title="📰 News Summarizer RAG", layout="centered")
st.title("🧠 RAG-Based News Summarizer")

input_type = st.radio("Choose input type:", ["Text", "URL", "PDF", "Image"])
input_data = ""
uploaded_file = None

if input_type == "Text":
    input_data = st.text_area("Enter your news text here:")
elif input_type == "URL":
    input_data = st.text_input("Paste a news article URL:")
elif input_type in ["PDF", "Image"]:
    uploaded_file = st.file_uploader(
        "Upload a file", type=["pdf"] if input_type == "PDF" else ["jpg", "jpeg", "png"]
    )

languages = {"English": "en", "Hindi": "hi", "Marathi": "mr"}
selected_lang = st.selectbox("Select response language:", list(languages.keys()))
play_audio = st.checkbox("🔊 Play voice response")

def get_extracted_text(input_type, input_data, uploaded_file):
    if input_type == "Text":
        return extract_text_from_text(input_data)
    elif input_type == "URL":
        return extract_text_from_url(input_data)
    elif input_type == "PDF":
        return extract_text_from_pdf(uploaded_file)
    elif input_type == "Image":
        return extract_text_from_image(uploaded_file)

if st.button("Summarize"):
    if input_type in ["Text", "URL"] and not input_data:
        st.warning("Please enter text or URL.")
    elif input_type in ["PDF", "Image"] and not uploaded_file:
        st.warning("Please upload a file.")
    else:
        try:
            with st.spinner("Extracting text..."):
                extracted_text = get_extracted_text(input_type, input_data, uploaded_file)
            st.text_area("Extracted Text", extracted_text, height=200)

            with st.spinner("Generating summary..."):
                responses = generate_response(
                    query_text=extracted_text,
                    target_languages=[languages[selected_lang]],
                    source_type=input_type.lower()
                )
                result = responses.get(languages[selected_lang], "No response.")

            st.markdown("### Summary:")
            st.write(result)

            if play_audio and result:
                tts = gTTS(text=result, lang=languages[selected_lang])
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp, format="audio/mp3")

        except Exception as e:
            st.error(f"Error: {e}")
