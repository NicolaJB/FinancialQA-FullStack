# backend/app/services/financialqa/pipeline.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

# -----------------------------
# CPU-friendly embedding model
# -----------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBEDDING_MODEL)

# -----------------------------
# Example placeholder documents
# -----------------------------
documents: List[dict] = []  # initially empty
doc_embeddings: np.ndarray = np.zeros((0, embedder.get_sentence_embedding_dimension()))
vectorstore = None  # will load at startup

# -----------------------------
# Similarity search function
# -----------------------------
def similarity_search(query: str, k: int = 3) -> List[Tuple[dict, float]]:
    """
    Return top-k most relevant documents along with similarity scores.
    """
    if len(documents) == 0:
        return []

    query_embedding = embedder.encode([query])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_idx = np.argsort(similarities)[::-1][:k]
    return [(documents[i], similarities[i]) for i in top_idx]

# -----------------------------
# Text splitting function
# -----------------------------
def split_texts(texts: List[str], chunk_size: int = 500) -> List[str]:
    """
    Split long documents into smaller chunks.
    """
    chunks = []
    for text in texts:
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size].strip()
            if chunk:
                chunks.append(chunk)
    return chunks

# -----------------------------
# Embed new documents
# -----------------------------
def embed_documents(text_chunks: List[str]) -> np.ndarray:
    """
    Generate embeddings for new text chunks and update the document store.
    """
    global doc_embeddings, documents
    if not text_chunks:
        return np.zeros((0, embedder.get_sentence_embedding_dimension()))

    new_embeddings = embedder.encode(text_chunks)
    doc_embeddings = np.vstack([doc_embeddings, new_embeddings]) if doc_embeddings.size else new_embeddings
    for idx, chunk in enumerate(text_chunks, start=len(documents)+1):
        documents.append({"id": idx, "page_content": chunk})
    return new_embeddings
