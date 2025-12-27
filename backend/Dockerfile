# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Install build dependencies
RUN apk add --no-cache bash git python3 make g++

# Copy only package files first to use Docker cache effectively
COPY frontend/package*.json ./
COPY frontend/postcss.config.js ./
COPY frontend/tailwind.config.js ./

# Install npm dependencies (cached if package.json unchanged)
RUN npm install --legacy-peer-deps

# Copy the rest of the frontend source
COPY frontend ./

# Build static frontend
RUN npm run build && npm run export

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage caching
COPY backend/requirements.txt ./

# Install Python dependencies (cached if requirements.txt unchanged)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim
WORKDIR /app/backend

# Copy backend
COPY --from=backend-build /app/backend /app/backend

# Copy frontend static export
COPY --from=frontend-build /app/frontend/out ./frontend

EXPOSE 8000

# Start backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
