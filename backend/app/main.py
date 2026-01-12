# app/main.py
"""
Main FastAPI application for the Financial QA API.

This module sets up and configures the backend API, including:

- Creating the FastAPI app instance.
- Serving the Next.js frontend (if `SERVE_FRONTEND` environment variable is set).
- Including the API router for query-related endpoints (`/api` prefix).
- Providing basic endpoints:
    - `/health`: Simple health check returning service status.
    - `/`: Root endpoint mirroring `/health`.
- Startup event to load, process, and embed documents from the `docs/` folder
  into the vector store used by the Financial QA pipeline.

The startup process:
1. Checks if the pipeline's vector store is initialized.
2. Reads `.txt` and `.pdf` files from the `docs/` directory.
3. Splits the documents into chunks suitable for embedding.
4. Embeds the text chunks and populates the vector store.
5. Prints progress and status messages for monitoring startup.

Dependencies:
- FastAPI for web API creation.
- PyPDF2 for PDF text extraction.
- app.services.financialqa.pipeline for document processing and embeddings.
- app.routers.query for API query routes.
- fastapi.staticfiles.StaticFiles for serving a frontend app.
"""
from pathlib import Path
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.routers.query import router as query_router
from app.services.financialqa import pipeline
from PyPDF2 import PdfReader

# Create FastAPI app
app = FastAPI(title="Financial QA API")

# Serve Next.js frontend if requested
FRONTEND_DIR = Path("frontend/.next")
if os.getenv("SERVE_FRONTEND") == "true" and FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend",
    )

# Include API routes
app.include_router(router=query_router, prefix="/api")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Root mirrors /health
@app.get("/")
def root():
    return JSONResponse(content={"status": "ok"})

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
