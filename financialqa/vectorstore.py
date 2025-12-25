# financialqa/vectorstore.py
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings

class VectorStore:
    def __init__(self, embedding_model: Embeddings):
        self.vectordb = None
        self.embedding_model = embedding_model

    def add_documents(self, docs: list):
        """Add documents (list of strings) to Chroma vector store."""
        self.vectordb = Chroma.from_texts(docs, embedding=self.embedding_model)

    def query_vector(self, query: str, top_k: int = 5):
        """Retrieve top_k most similar documents for a query."""
        if not self.vectordb:
            raise ValueError("Vector store is empty. Add documents first.")
        return self.vectordb.similarity_search(query, k=top_k)
