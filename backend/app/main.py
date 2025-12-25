# app/main.py
from pathlib import Path
from fastapi import FastAPI
from app.routers.query import router as query_router
from app.services.financialqa import pipeline
from PyPDF2 import PdfReader
from transformers import pipeline as hf_pipeline

app = FastAPI(title="Financial QA API")

# ---------------------------
# API routes
# ---------------------------
app.include_router(router=query_router, prefix="/api")

# ---------------------------
# Test endpoint
# ---------------------------
@app.get("/test")
def test():
    return {"ok": True}

# ---------------------------
# Startup event
# ---------------------------
@app.on_event("startup")
def startup_event():
    print("Starting Financial QA API...")

    # ---------------------------
    # Load documents from /docs
    # ---------------------------
    if pipeline.vectorstore is None:
        all_texts = []
        DOCS_FOLDER = Path(__file__).parent.parent / "docs"
        if DOCS_FOLDER.exists() and DOCS_FOLDER.is_dir():
            for file in DOCS_FOLDER.iterdir():
                try:
                    text = ""
                    if file.suffix.lower() == ".txt":
                        with open(file, "r", encoding="utf-8") as f:
                            text = f.read().strip()
                    elif file.suffix.lower() == ".pdf":
                        reader = PdfReader(file)
                        text = "".join([p.extract_text() or "" for p in reader.pages]).strip()

                    if text:
                        all_texts.append(text)
                        print(f"Loaded {file.name} ({len(text)} chars)")
                except Exception as e:
                    print(f"Failed to read {file.name}: {e}")

        # Split into chunks and embed
        if all_texts:
            chunks = pipeline.split_texts(all_texts)
            pipeline.embed_documents(chunks)
            print(f"Embedded {len(chunks)} text chunks.")
            pipeline.vectorstore = True  # mark as loaded

    print("Financial QA API startup complete.")
