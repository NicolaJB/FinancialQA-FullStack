# financialqa/embeddings.py
from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingsGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Initializing embeddings model: {model_name}...")
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def generate_embeddings(self, docs: list[str]) -> list[list[float]]:
        """
        Converts a list of documents (strings) into embeddings.
        Returns a list of vectors.
        """
        return self.model.embed_documents(docs)

    def embed_query(self, query: str) -> list[float]:
        """
        Generate embedding for a single query.
        """
        return self.model.embed_query(query)
