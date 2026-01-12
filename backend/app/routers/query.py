# backend/app/routers/query.py
"""
Query API router for the Financial QA backend.

This module defines the `/query` endpoint for retrieving
relevant information from embedded documents using the
Financial QA pipeline. It includes:

- Request model: `QueryRequest` for validating incoming queries.
- Endpoint: `/query` for submitting a textual query and receiving
  a summarized response from relevant document chunks.

Workflow of the `/query` endpoint:
1. Validate that the query text is non-empty.
2. Check if the document vector store is initialised; if not, return a
   safe "not ready" message.
3. Perform a similarity search on the vector store to retrieve the top-k
   relevant document chunks.
4. Extract text content from the retrieved chunks.
5. Summarise the combined content using the CPU-based summariser.
6. Return the summarised result. Any errors during processing are
   caught and returned safely without crashing the API.

Dependencies:
- FastAPI for endpoint creation.
- Pydantic for request validation.
- `pipeline` from `app.services.financialqa` for vector search.
- `cpu_summarize` from `app.services.summarizer` for summarization.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.financialqa import pipeline
from app.services.summarizer import cpu_summarize

router = APIRouter()


# ---------------------------
# Request model
# ---------------------------
class QueryRequest(BaseModel):
    query: str


# ---------------------------
# Query endpoint
# ---------------------------
@router.post("/query")
async def query_docs(request: QueryRequest):
    query_text = request.query.strip()

    if not query_text:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # ---- SAFETY CHECK ----
    if pipeline.vectorstore is None:
        return {
            "summary": "Document index not ready. Please try again shortly."
        }

    try:
        # Retrieve top-k relevant chunks
        results = pipeline.similarity_search(query_text, k=5)

        if not results:
            return {"summary": "No relevant documents found."}

        # Extract text content
        chunk_texts = [
            doc["page_content"][:1000]
            for doc, _score in results
            if "page_content" in doc
        ]

        if not chunk_texts:
            return {"summary": "No usable document content found."}

        combined_text = " ".join(chunk_texts)

        summary = cpu_summarize(combined_text)

        return {
            "summary": summary.strip()
        }

    except Exception as e:
        # Fail safely without killing the API
        return {
            "summary": "An error occurred while processing the query.",
            "error": str(e)
        }
