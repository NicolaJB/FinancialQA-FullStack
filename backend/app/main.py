# app/main.py
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.query import router as query_router
from app.services.financialqa import pipeline

# Create FastAPI app first
app = FastAPI(title="Financial QA API")

# Serve Next.js frontend from correct path inside container
import os

FRONTEND_DIR = Path("frontend/.next")

if os.getenv("SERVE_FRONTEND") == "true" and FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend",
    )

# API routes
app.include_router(router=query_router, prefix="/api")

# Test endpoint
@app.get("/test")
def test():
    return {"ok": True}

# Startup event
@app.on_event("startup")
def startup_event():
    print("Financial QA API starting...")

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
                        from PyPDF2 import PdfReader
                        reader = PdfReader(file)
                        text = "".join([p.extract_text() or "" for p in reader.pages]).strip()

                    if text:
                        all_texts.append(text)
                        print(f"Loaded {file.name} ({len(text)} chars)")
                except Exception as e:
                    print(f"Failed to read {file.name}: {e}")

        if all_texts:
            chunks = pipeline.split_texts(all_texts)
            pipeline.embed_documents(chunks)
            pipeline.vectorstore = True
            print(f"Embedded {len(chunks)} text chunks.")

    print("Financial QA API startup complete.")
