# backend/app/routers/query.py
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
