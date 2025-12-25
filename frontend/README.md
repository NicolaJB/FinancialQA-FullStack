# Financial QA – Document-Based Question Answering

This application allows you to ask financial questions in plain English and receive answers extracted from your own uploaded text documents, such as earnings reports or analyst notes.  
It uses **FastAPI** and **LangChain** with **FAISS** for embeddings, and a **Next.js** frontend for the user interface.

---

## Features
- Upload `.txt` documents (earnings reports, financial metrics, etc.) into the `/docs` folder.
- Documents are embedded into a FAISS vectorstore on startup for fast similarity search.
- Query the embedded knowledge base using natural-language questions.
- Next.js frontend for an easy-to-use interface.
- Returns the top relevant text chunks from your documents.

---

## Project Structure
```bash
financial-qa/
├── app.py # FastAPI backend
├── financialqa/
│ ├── pipeline.py # Embedding and FAISS persistence
│ └── faiss_index/ # Saved vectorstore (automatically created)
├── docs/ # Your .txt documents
│ ├── apple_q3_2024.txt
│ ├── amazon_q3_2024.txt
│ └── ...
financial-qa-frontend/
├── app/api/query/route.ts # Next.js API route (proxy to FastAPI)
└── app/components/QueryForm.tsx # React form to submit queries
````


---

## Installation

### Backend (FastAPI)

Create a Python environment and install dependencies:

```bash
cd financial-qa
pip install -r requirements.txt
# or install individually:
pip install fastapi uvicorn langchain faiss-cpu sentence-transformers
```
Frontend (Next.js)
```bash
cd financial-qa-frontend
npm install
```
Running the Application

Start FastAPI backend:
```bash
cd financial-qa
uvicorn app:app --reload --port 8000
```
You should see output similar to:
```bash
Loaded vectorstore from /financialqa/faiss_index
Embedding 23 documents and saving to /financialqa/faiss_index
Application startup complete.
```
Start Next.js frontend:
```bash
cd financial-qa-frontend
npm run dev
```
Open http://localhost:3000 in your browser.

## Usage
Place your .txt files into the docs/ folder.

Restart the FastAPI server to embed any new documents.

Open the web interface, type a financial question (e.g., “Summarise Tesla’s Q2 2025 earnings report”), and press Submit.

The application will return the most relevant chunks from your embedded documents.

## How It Works
pipeline.py uses HuggingFaceEmbeddings to convert document chunks into vectors.

Vectors are stored in a FAISS index saved to disk.

When queried, the system retrieves the most similar chunks to your question.

No external API key is required; embeddings are generated locally.

## Adding More Documents
Add additional .txt files into docs/ and restart uvicorn. The backend will automatically embed them into the FAISS index.
For incremental updates without a restart, embed_documents() can be called manually via a FastAPI endpoint.

## Configuration
DOCS_FOLDER is defined in app.py.

The embedding model can be changed in pipeline.py (default: sentence-transformers/all-MiniLM-L6-v2).

## License
MIT License. You are free to adapt and extend this project.

## Credits
- FastAPI
- LangChain
- FAISS
- Next.js
- vbnet
