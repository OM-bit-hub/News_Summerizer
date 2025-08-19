import os
import streamlit as st
from extractor import extract_text_from_url, extract_text_from_pdf, extract_text_from_image
from retriever import NewsRetriever
from generator import DualGenerator
from evaluator import SummaryEvaluator
from tts import text_to_speech, LANG_CODES
from news_classifier import NewsClassifier

st.set_page_config(
    page_title="📰 RAG News Summarizer",
    layout="wide",
    page_icon="📰"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            max-width: 90%;
        }
        
        /* Clean title */
        .main-title {
            font-size: 32px;
            font-weight: 600;
            color: #1f2937;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            text-align: center;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        
        /* Simple cards */
        .input-section, .output-section {
            background: #f8fafc;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #e5e7eb;
            margin-bottom: 1rem;
        }
        
        /* Section headers */
        .section-title {
            font-size: 18px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #3b82f6;
        }
        
        /* Better form elements */
        .stSelectbox > div > div {
            border-radius: 8px;
        }
        
        .stTextArea textarea, .stTextInput input {
            border-radius: 8px !important;
            border: 1px solid #d1d5db !important;
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* Clean button */
        .stButton > button {
            background-color: #3b82f6 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.5rem !important;
            transition: background-color 0.2s !important;
        }
        
        .stButton > button:hover {
            background-color: #2563eb !important;
        }
        
        /* File uploader */
        .stFileUploader > div {
            border-radius: 8px;
            border: 2px dashed #d1d5db;
        }
        
        /* Status messages */
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 8px !important;
        }
        
        /* Output areas */
        .output-box {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main-title {
                font-size: 24px;
            }
            .input-section, .output-section {
                padding: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📰 RAG Based News Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered news summarization with multi-language support</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("""
        <div class="input-section">
            <div class="section-title">📥 Input</div>
        </div>
    """, unsafe_allow_html=True)
    
    input_mode = st.selectbox("Input Type", ["Text", "URL", "PDF", "Image"])
    user_input = None

    if input_mode == "Text":
        user_input = st.text_area(
            "Enter news content:",
            height=120,
            placeholder="Paste your news article here..."
        )
    elif input_mode == "URL":
        url = st.text_input("Website URL:", placeholder="https://example.com/news")
        if url:
            try:
                with st.spinner("Extracting content..."):
                    user_input = extract_text_from_url(url)
                if user_input:
                    st.success(f"Extracted {len(user_input.split())} words")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    elif input_mode == "PDF":
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_pdf:
            try:
                with st.spinner("Processing PDF..."):
                    user_input = extract_text_from_pdf(uploaded_pdf.read())
                if user_input:
                    st.success(f"✅ Extracted {len(user_input.split())} words")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    elif input_mode == "Image":
        uploaded_img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_img:
            try:
                with st.spinner("Extracting text..."):
                    user_input = extract_text_from_image(uploaded_img.read())
                if user_input:
                    st.success(f"✅ Extracted {len(user_input.split())} words")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    st.markdown("---")
    
    # Settings
    col_lang, col_adv = st.columns([1, 1])
    
    with col_lang:
        tts_language = st.selectbox("Output Language", ["English", "Hindi", "Marathi"])
    
    with col_adv:
        show_reference = st.checkbox("Add Reference Summary")
    
    if show_reference:
        reference = st.text_area(
            "Reference Summary (optional):",
            height=80,
            placeholder="Optional reference for evaluation..."
        )
    else:
        reference = ""

    st.markdown("---")
    summarize_btn = st.button("🚀 Generate Summary", use_container_width=True)


with col2:
    st.markdown("""
        <div class="output-section">
            <div class="section-title">📄 Results</div>
        </div>
    """, unsafe_allow_html=True)
    
    # placeholders
    summary_placeholder = st.empty()
    audio_placeholder = st.empty()
    scores_placeholder = st.empty()


if summarize_btn:
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please provide input content.")
    else:
        # progress indicator
        with st.status("Processing...", expanded=True) as status:
            st.write("🔎 Checking if content is news-related...")
            classifier = NewsClassifier()
            
            if not classifier.is_news(user_input):
                st.error("🚫 Content doesn't appear to be news-related.")
                status.update(label="❌ Processing failed", state="error")
            else:
                st.write("🔍 Finding relevant articles...")
                retriever = NewsRetriever()
                docs = retriever.search(user_input, n_results=3)

                st.write(f"🧠 Generating summary in {tts_language}...")
                generator = DualGenerator()
                summaries = generator.generate_summaries(user_input, docs, tts_language)

                # Use retrieved docs as reference if none provided
                if not reference.strip():
                    reference = "\n".join(docs)
                    st.write("ℹ️ Using retrieved articles for evaluation")

                st.write("📊 Evaluating quality...")
                eval_summaries = summaries.get("english", summaries)
                display_summaries = summaries.get("final", summaries)

                evaluator = SummaryEvaluator()
                scores = evaluator.evaluate_all(eval_summaries, reference)
                best_model = evaluator.select_best_summary(scores)
                best_summary = display_summaries[best_model]

                st.write("🎵 Generating audio...")
                audio_file = text_to_speech(best_summary, lang=LANG_CODES[tts_language])
                
                
                status.update(label="✅ Complete!", state="complete")

                # Display results
                with summary_placeholder:
                    st.markdown("### 📝 Summary")
                    st.info(f"**Best Model:** {best_model.upper()} | **Language:** {tts_language} | **Words:** {len(best_summary.split())}")
                    st.text_area("Generated Summary:", best_summary, height=200)

    
                with audio_placeholder:
                    st.markdown("### 🔊 Audio")
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                    else:
                        st.write("No audio available.")
                        
st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; color: #6b7280; padding: 1rem;'>
        🤖 Powered by RAG Technology | 🌍 Multi-Language Support <br>
        👨‍💻 Created by 
        <a href='https://github.com/OM-bit-hub' target='_blank' style='color: #2563eb; text-decoration: none;'>Om Dhengle</a> 
        and 
        <a href='https://github.com/Riteshtaru343/RAG_Based_News_Summerizer.git' target='_blank' style='color: #2563eb; text-decoration: none;'>Ritesh Taru</a>
    </div>
    """,
    unsafe_allow_html=True
)


