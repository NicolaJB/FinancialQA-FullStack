# Financial QA Application

A full-stack **Financial Question Answering (QA) app** that lets users query financial documents using semantic search and a CPU-friendly summariser.

The system embeds `.txt` and `.pdf` documents into a vector store and generates concise summaries for relevant chunks via a web interface.

## Tech Stack
- **Backend:** FastAPI  
- **Frontend:** Next.js (App Router) + React  
- **Styling:** Tailwind CSS  
- **LLM & Summarizer:** HuggingFace Transformers (`distilBART`)  
- **Vector Store:** In-memory FAISS embeddings  
- **API Communication:** Frontend API routes proxy requests to FastAPI  

## Features
- Load `.txt` and `.pdf` financial documents from disk  
- Chunk documents and embed for semantic search  
- Retrieve top-k relevant document chunks  
- CPU-friendly summarization of retrieved chunks  
- Responsive web UI with proxy API layer  
- Health check endpoint for backend

## Repository Structure
```bash
Financial-QA-FullStack/
├── backend/
│ ├── app/main.py
│ ├── routers/query.py
│ └── services/financialqa/pipeline.py
│ └── services/summarizer.py
│ └── docs/
│ └── requirements.txt
├── frontend/
│ ├── app/layout.tsx
│ ├── app/page.tsx
│ ├── app/api/query/route.ts
│ └── components/QueryForm.tsx
│ └── globals.css
│ └── package.json
└── README.md
```
## Prerequisites
- Python 3.9+  
- Node.js 18+ (includes npm)
## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
cd .. # requirements.txt is in root directory
pip install -r requirements.txt
```
Add your .txt or .pdf files to backend/docs/.

### Run the backend:

```bash
python -m uvicorn app.main:app --reload --port 8000
````
### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:3000 in a browser.

### API Endpoints
Query: POST /api/query

Request example:

```json
{ "query": "Summarize Tesla" }
```

Response example:
```json
{ "summary": "Tesla, founded in 2003, focuses on electric vehicles and renewable energy..." }
```
Health Check: GET /test

Response: 
```
{ "ok": true }
```
### Usage

- Start backend: uvicorn app.main:app --reload --port 8000
- Start frontend: npm run dev
- Open browser at http://localhost:3000
- Enter a financial question and submit

Flow:
```
Browser → Next.js API route → FastAPI → Vectorstore + Summarizer → JSON → UI
```
Development Notes:

- Frontend queries are proxied to backend via /api/query
- Vectorstore is loaded at startup; summarization runs on CPU
- Frontend and backend run independently

### Future Improvements
- Upload documents via frontend
- Metadata & citation tracking
- Streaming summarisation 
- Authentication & rate limiting
- Cloud deployment & Docker support

### License
Educational and demonstration purposes. Free to use, modify, and extend.