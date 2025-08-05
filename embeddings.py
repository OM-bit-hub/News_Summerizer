from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from functools import lru_cache

@lru_cache(maxsize=1)
def get_vectorstore():
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory="chroma_store", embedding_function=embedding)

vectorstore = get_vectorstore()

def add_to_vectorstore(text, metadata=None):
    if not text.strip():
        return
    existing = vectorstore.similarity_search(text, k=1)
    if existing and existing[0].page_content.strip() == text.strip():
        return
    vectorstore.add_texts([text], metadatas=[metadata] if metadata else [{}])
    vectorstore.persist()

def get_relevant_docs(query, k=4):
    if not query.strip():
        return []
    return vectorstore.similarity_search(query.strip(), k=k)
