# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
RUN apk add --no-cache bash git python3 make g++

COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
RUN npm install --legacy-peer-deps

COPY frontend/public ./public
COPY frontend/src ./src
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

COPY --from=backend-build /app/backend /app/backend
COPY --from=frontend-build /app/frontend/out ./frontend

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
