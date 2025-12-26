# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Install required build tools for Alpine
RUN apk add --no-cache bash git python3 make g++

# Copy package files
COPY frontend/package*.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Clean npm cache and install dependencies, including tailwindcss and fonts
RUN npm cache clean --force && \
    npm install --legacy-peer-deps && \
    npm install tailwindcss --legacy-peer-deps && \
    npm install @fontsource/geist @fontsource/geist-mono

# Debug step: List the contents of the node_modules directory to check installed packages
RUN ls -R node_modules

# Copy source code
COPY frontend/public ./public
COPY frontend/src ./src

# Build the Next.js frontend
RUN npm run build

# ---- Stage 2: Build Backend ----
FROM python:3.11-slim AS backend-build

WORKDIR /app/backend

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend ./

# ---- Stage 3: Final Image ----
FROM python:3.11-slim

WORKDIR /app

# Copy backend from build stage
COPY --from=backend-build /app/backend /app/backend

# Copy frontend build output
COPY --from=frontend-build /app/frontend/.next /app/frontend/.next
COPY --from=frontend-build /app/frontend/public /app/frontend/public
COPY --from=frontend-build /app/frontend/package*.json /app/frontend/package*.json
COPY --from=frontend-build /app/frontend/node_modules /app/frontend/node_modules

# Set working directory for backend
WORKDIR /app/backend

# Expose backend port (adjust if needed)
EXPOSE 8000

# Command to run backend
CMD ["python", "main.py"]
