import chromadb
from datetime import datetime
from embeddings import get_embedding
import logging

logger = logging.getLogger(__name__)
persist_directory = "./chroma_store"
chroma_client = chromadb.PersistentClient(path=persist_directory)
collection = chroma_client.get_or_create_collection(name="news_collection")

def add_to_memory(text, source_type="text", metadata_extra=None, skip_if_duplicate=True):
    try:
        if not text.strip():
            return False

        if skip_if_duplicate:
            existing = search_memory(text, n_results=1)
            if existing and existing[0].strip() == text.strip():
                logger.info("Duplicate found. Skipping memory addition.")
                return False

        embedding = get_embedding(text)
        now = datetime.utcnow()
        doc_id = f"{source_type}_{now.isoformat()}"

        metadata = {
            "source": source_type,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if metadata_extra:
            metadata.update(metadata_extra)

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[doc_id],
            metadatas=[metadata]
        )
        logger.info(f"Document added to memory: {doc_id}")
        return True
    except Exception as e:
        logger.error(f"[Error adding to memory]: {e}")
        return False

def search_memory(query, n_results=5):
    try:
        if not query.strip():
            return []
        embedding = get_embedding(query)
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            include=['documents']
        )
        documents = results['documents'][0] if results['documents'] else []
        return documents
    except Exception as e:
        logger.error(f"[Error searching memory]: {e}")
        return []
