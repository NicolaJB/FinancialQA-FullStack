# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Install build tools
RUN apk add --no-cache bash git python3 make g++

# Copy package files and install dependencies
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
RUN npm install --legacy-peer-deps && \
    npm install tailwindcss --legacy-peer-deps && \
    npm install @fontsource/geist @fontsource/geist-mono

# Copy frontend source code
COPY frontend/public ./public
COPY frontend/src ./src

# Build frontend (production)
RUN npm run build

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build

WORKDIR /app/backend

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
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

# Copy frontend build (.next + public + node_modules) inside backend folder
COPY --from=frontend-build /app/frontend/.next ./frontend/.next
COPY --from=frontend-build /app/frontend/public ./frontend/public
COPY --from=frontend-build /app/frontend/node_modules ./frontend/node_modules

# Expose port
EXPOSE 8000

# Run backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
