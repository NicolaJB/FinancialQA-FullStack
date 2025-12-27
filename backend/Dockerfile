# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Allow build-time env variables
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Install dependencies for building
RUN apk add --no-cache bash git python3 make g++

# Copy package files and configs
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

RUN npm install --legacy-peer-deps

# Copy source code
COPY frontend/public ./public
COPY frontend/app ./app  # Next 13+ "app" dir
COPY frontend/pages ./pages  # if using pages directory
COPY frontend/components ./components

# Build + export static site
RUN npm run build && npm run export

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build
WORKDIR /app/backend

RUN apt-get update && apt-get install -y build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim
WORKDIR /app/backend

# Copy backend
COPY --from=backend-build /app/backend /app/backend

# Copy frontend static export
COPY --from=frontend-build /app/frontend/out ./frontend

EXPOSE 8000

# Start the backend
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
