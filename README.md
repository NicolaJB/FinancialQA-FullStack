# Financial QA Application

A full-stack **Financial Question Answering (QA)** application that allows users to query financial documents using semantic search and a CPU-friendly summariser.

The system embeds `.txt` and `.pdf` documents into a vector store and generates concise summaries for relevant chunks via a web interface.

## Tech Stack
- **Backend:** FastAPI  
- **Frontend:** Next.js (App Router) + React  
- **Styling:** Tailwind CSS  
- **LLM & Summariser:** HuggingFace Transformers (`distilBART`)  
- **Vector Store:** In-memory FAISS embeddings  
- **API Communication:** Frontend API routes proxy requests to FastAPI  

## Features
- Load `.txt` and `.pdf` financial documents from disk  
- Chunk documents and embed for semantic search  
- Retrieve top-k relevant document chunks  
- CPU-friendly summarisation of retrieved chunks  
- Responsive web UI with proxy API layer  
- Health check endpoint for backend

## Repository Structure
```bash
Financial-QA-FullStack/
├── backend/
│   ├── Dockerfile                  # Backend Dockerfile
│   ├── app/main.py
│   ├── app/routers/query.py
│   ├── app/services/financialqa/
│   │   ├── config.py
│   │   ├── faiss_index.py
│   │   ├── tiny_dataset.py
│   │   ├── vectorstore.py
│   │   ├── embed_docs.py
│   │   ├── pipeline.py
│   │   ├── transcription.py
│   │   ├── classifier.py
│   │   ├── embeddings.py
│   │   ├── rag_pipeline.py
│   │   └── utils.py
│   ├── app/services/summarizer.py
│   ├── app/docs/
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile                  # Frontend Dockerfile
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── api/
│   │   │   └── query/route.ts
│   │   └── components/
│   │       ├── QueryForm.tsx
│   │       └── QueryResults.tsx
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── postcss.config.js
│   ├── postcss.config.mjs
│   ├── eslint.config.mjs
│   └── README.md
├── .github/workflows/docker-build.yml
└── README.md
```
## Prerequisites
- Python 3.9+  
- Node.js 18+ (includes npm)

## Setup

### Backend
```bash
cd backend

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies explicitly
pip install "numpy<2"
pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu

# Install remaining backend dependencies
pip install -r requirements.txt
```
Add your .txt and/or .pdf files to:
```
backend/docs/
```
### Run the Backend
```
cd backend
source venv/bin/activate   # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
Open http://localhost:8000 to verify the backend is running.

### Install & Run the Frontend
```
cd frontend
npm install  
npm run dev 
```
> Ensure fonts are installed: `npm install @fontsource/geist @fontsource/geist-mono`
## Heath Check Test
The backend includes a simple health check test to verify the API is running correctly.
```bash
# Activate virtual environment if not already active
cd backend
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install pytest
# Run the health check
python -m pytest -v tests/test_health.py
```
Expected Output:
```
======================================================================= test session starts =======================================================================
collected 1 item                                                                                                                                                  

tests/test_health.py::test_health_endpoint PASSED                                                                                                           [100%]

======================================================================== 1 passed in 0.85s ==================================================================
```
- PASSED indicates the backend is running and the /health endpoint responds correctly.
- If any test shows FAILED, the API may not be running or the endpoint returned an unexpected response.

### API Endpoints

#### Query
- **Endpoint:** `POST /api/query`  
- **Description:** Submit a financial question and receive a summarised answer from relevant document chunks.  
- **Usage:** Must be a **POST** request with JSON body. GET requests are **not allowed**.

**Request (cURL):**
```bash
cd backend
source venv/bin/activate 

curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Summarise Tesla"}'
```
*Request example:*
```json
{
  "query": "Summarise Tesla"
}
```
*Response example:*

```json
{
  "summary": "Tesla, founded in 2003, focuses on electric vehicles and renewable energy..."
}
```
### Health Check
- Endpoint: GET /test
- Description: Simple endpoint to verify that the backend is running. curl http://localhost:8000/health
```bash
cd backend
source venv/bin/activate 

curl http://localhost:8000/health
````
*Response example:*
```
{ "ok": true }
```
### Usage
1. Start backend:
```bash
cd backend
source venv/bin/activate   # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
````
2. Start frontend: 
```bash
cd frontend
npm run dev
```
3. Open in Browser:

Navigate to http://localhost:3000 and enter a financial question e.g. "Key points for Apple’s latest 10-Q"

###  Flow:
```
Browser → Next.js API route → FastAPI → Vectorstore + Summarizer → JSON → UI
```
### Development Notes:
- Frontend queries are proxied to the backend via /api/query
- Vectorstore is loaded on backend startup; summarisation runs on CPU. 
- Frontend and backend run independently for local development.

## Docker and GitHub Actions
This repository includes Dockerfiles for both the backend and frontend services, along with automated **GitHub Actions workflows** to build and push the images.


### Backend Dockerfile
- **Location:** `backend/Dockerfile`  
- **Base Image:** `python:3.11-slim`  
- **Purpose:** Builds the FastAPI backend for Financial QA.  
- **Key Steps:**
  1. Install system dependencies (`build-essential`, `git`, `curl`, `bash`).
  2. Install Python dependencies from `backend/requirements.txt`.
  3. Copy backend source code.
  4. Expose port `8000` for the API.
  

### Frontend Dockerfile
- **Location:** `frontend/Dockerfile`  
- **Base Image:** `node:lts` (or Node version you specify)  
- **Purpose:** Builds the Next.js frontend.  
- **Key Steps:**
  1. Install Node dependencies from `package.json`.
  2. Build the Next.js application.
  3. Serve the production build (`.next`).
  4. Expose port `3000` for the frontend.
  

### GitHub Actions Workflows

This repository includes a GitHub Actions workflow that **builds and pushes Docker images** for both the backend and frontend services whenever code is pushed to `main`.

#### Backend Workflow
- **Location:** `.github/workflows/docker-build.yml`
- **Purpose:** Builds and pushes the backend image (`nicolajb/financialqa-fullstack:latest`).  
- **Runner:** `ubuntu-latest`  
- **Steps:**
  1. Checkout repository (`actions/checkout@v3`)
  2. Set up Docker Buildx (`docker/setup-buildx-action@v3`)
  3. Login to Docker Hub using secrets:
     - `DOCKER_HUB_USERNAME`
     - `DOCKER_HUB_ACCESS_TOKEN`
  4. Build and push Docker image using `backend/Dockerfile`

#### Frontend Workflow
- **Location:** Included as an additional job in the backend workflow
- **Purpose:** Builds and pushes the frontend image (`nicolajb/financialqa-frontend:latest`)  
- **Steps:**
  1. Checkout repository
  2. Set up Docker Buildx
  3. Login to Docker Hub
  4. Build and push Docker image using `frontend/Dockerfile`



### Future Improvements
- Upload documents via frontend
- Metadata & citation tracking
- Streaming summarisation 
- Authentication & rate limiting

### License
MIT License