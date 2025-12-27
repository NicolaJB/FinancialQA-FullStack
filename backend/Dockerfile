# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Install dependencies for building
RUN apk add --no-cache bash git python3 make g++

# Copy package files
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Install npm dependencies
RUN npm install --legacy-peer-deps

# Copy app code
COPY frontend/public ./public
COPY frontend/app ./app      # Match your actual folder structure

# Build + export static site
RUN npm run build && npm run export

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build
WORKDIR /app/backend

RUN apt-get update && apt-get install -y build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim
WORKDIR /app/backend

# Copy backend from build stage
COPY --from=backend-build /app/backend /app/backend

# Copy frontend static export
COPY --from=frontend-build /app/frontend/out /app/frontend

# Expose port
EXPOSE 8000

# Start backend
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
