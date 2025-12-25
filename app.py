# app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from financialqa.pipeline import (
    embed_documents,
    load_vectorstore,
    vectorstore,
    query_vectorstore,
)

# --- CONFIG ---
DOCS_FOLDER = "/Users/nicolabuttigieg/PycharmProjects/financial-qa/docs"

# --- FASTAPI APP ---
app = FastAPI(title="Financial QA API")

# --- MODELS ---
class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 3


# --- HELPERS ---
def load_and_embed_docs():
    """Load .txt documents from DOCS_FOLDER and embed them if needed."""
    docs = []
    if os.path.exists(DOCS_FOLDER) and os.path.isdir(DOCS_FOLDER):
        for file in os.listdir(DOCS_FOLDER):
            if file.endswith(".txt"):
                path = os.path.join(DOCS_FOLDER, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        docs.append(f.read())
                except Exception as e:
                    print(f"Failed to read {file}: {e}")
    else:
        print(f"DOCS_FOLDER {DOCS_FOLDER} not found or is not a directory.")

    if docs:
        embed_documents(docs)
    else:
        print("No .txt documents found. Vectorstore remains empty.")


# --- STARTUP ---
@app.on_event("startup")
def startup_event():
    # Try loading existing index
    load_vectorstore()
    # Only embed if we couldn't load
    if vectorstore is None:
        load_and_embed_docs()


# --- ROUTES ---
@app.get("/")
def root():
    return {"message": "Financial QA API is running. Use POST /query"}


@app.post("/query")
def query_financial_qa(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        results = query_vectorstore(req.query, k=req.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"query": req.query, "answer_chunks": results}
