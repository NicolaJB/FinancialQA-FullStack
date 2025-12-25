# Financial-QA-FullStack/financialqa/pipeline.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

# CPU-friendly embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBEDDING_MODEL)

# Example documents
documents = [
    {"id": 1, "page_content": "The stock market crashed in 2008."},
    {"id": 2, "page_content": "Inflation affects purchasing power."},
    {"id": 3, "page_content": "Diversification reduces investment risk."},
]

# Generate embeddings
doc_embeddings = embedder.encode([doc["page_content"] for doc in documents])

# Simple vectorstore flag
vectorstore = True

# Similarity search
def similarity_search(query: str, k: int = 3) -> List[dict]:
    query_embedding = embedder.encode([query])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_idx = np.argsort(similarities)[::-1][:k]
    return [documents[i] for i in top_idx]

# Text splitting
def split_texts(texts: List[str], chunk_size: int = 500) -> List[str]:
    chunks = []
    for text in texts:
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size].strip()
            if chunk:
                chunks.append(chunk)
    return chunks

# Embed new documents
def embed_documents(text_chunks: List[str]) -> np.ndarray:
    global doc_embeddings, documents
    new_embeddings = embedder.encode(text_chunks)
    doc_embeddings = np.vstack([doc_embeddings, new_embeddings])
    for idx, chunk in enumerate(text_chunks, start=len(documents)+1):
        documents.append({"id": idx, "page_content": chunk})
    return new_embeddings
