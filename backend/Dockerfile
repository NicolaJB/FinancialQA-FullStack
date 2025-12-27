# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Install build tools
RUN apk add --no-cache bash git python3 make g++

# Copy package files and install dependencies
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
RUN npm install --legacy-peer-deps

# Copy frontend source code
COPY frontend/public ./public
COPY frontend/src ./src

# Pass NEXT_PUBLIC_API_URL to frontend build
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build frontend (production)
RUN npm run build && npm run export

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build

WORKDIR /app/backend

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim

WORKDIR /app/backend

# Copy backend
COPY --from=backend-build /app/backend /app/backend

# Copy frontend build output
COPY --from=frontend-build /app/frontend/out ./frontend

# Expose port
EXPOSE 8000

# Run backend
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
