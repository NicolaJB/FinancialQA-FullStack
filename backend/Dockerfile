# ---- Base Image ----
FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential git curl bash \
    && rm -rf /var/lib/apt/lists/*

# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Install build dependencies
RUN apk add --no-cache bash git python3 make g++

# Copy package files and install dependencies
COPY frontend/package*.json ./
COPY frontend/postcss.config.js ./
COPY frontend/tailwind.config.js ./
RUN npm install --legacy-peer-deps

# Copy frontend source
COPY frontend ./

# Build frontend (no `next export` needed with `output: 'export'` in next.config.js)
RUN npm run build

# ---- Stage 2: Final Image ----
FROM base
WORKDIR /app/backend

# Install backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend ./

# Copy frontend build output
COPY --from=frontend-build /app/frontend/out ./frontend

EXPOSE 8000

# Start backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
