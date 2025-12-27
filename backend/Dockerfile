# ---- Stage 1: Optional Frontend Build ----
ARG BUILD_FRONTEND=false
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Install build dependencies
RUN apk add --no-cache bash git python3 make g++

# Copy package files for caching
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

RUN npm install --legacy-peer-deps

# Copy frontend source
COPY frontend ./

# Build + export only if BUILD_FRONTEND is true and frontend app exists
RUN if [ "$BUILD_FRONTEND" = "true" ] && [ -d "./app" ]; then \
      npm run build && npm run export; \
    else \
      echo "Skipping frontend build"; \
    fi

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

# Copy frontend static export if it exists
COPY --from=frontend-build /app/frontend/out ./frontend 2>/dev/null || echo "No frontend export"

EXPOSE 8000

# Start backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
