# ---- Base Image ----
FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git curl bash \
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

# Build frontend (next.config.js already has output: 'export')
RUN npm run build

# ---- Stage 2: Backend & Final Image ----
FROM base AS backend-build
WORKDIR /app/backend

# Copy backend minimal requirements
COPY backend/requirements.txt ./

# Upgrade pip and install dependencies
# Use --no-cache-dir to save space
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copy backend source
COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim
WORKDIR /app

# Copy backend from previous stage
COPY --from=backend-build /app/backend ./

# Copy frontend build output
COPY --from=frontend-build /app/frontend/out ./frontend

EXPOSE 8000

# Start backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
