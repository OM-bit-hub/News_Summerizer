import chromadb
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

class NewsRetriever:
    def __init__(self, chroma_path="chroma_store", collection_name="news_collection"):
        # Updated client initialization
        self.client = PersistentClient(path=chroma_path)

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(name=collection_name)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query: str, n_results: int = 5):
        query_embedding = self.model.encode([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results['documents'][0]  


