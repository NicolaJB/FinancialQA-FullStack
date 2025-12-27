# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Install required build tools for Alpine
RUN apk add --no-cache bash git python3 make g++

# Copy package files
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Install dependencies
RUN npm cache clean --force && \
    npm install --legacy-peer-deps && \
    npm install tailwindcss --legacy-peer-deps && \
    npm install @fontsource/geist @fontsource/geist-mono

# Copy source code
COPY frontend/public ./public
COPY frontend/src ./src

# Build the Next.js frontend (production build)
RUN npm run build
RUN npm run export   # Generates static files in /frontend/out

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build

WORKDIR /app/backend

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim

WORKDIR /app

# Copy backend from build stage
COPY --from=backend-build /app/backend /app/backend

# Copy static frontend build
COPY --from=frontend-build /app/frontend/out ./static

# Set working directory for backend
WORKDIR /app/backend

# Expose backend port
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
