# ---- Base Image ----
FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential git curl bash \
    && rm -rf /var/lib/apt/lists/*

# ---- Stage 1: Final Image ----
FROM base
WORKDIR /app/backend

# Copy backend requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copy backend source
COPY . .

EXPOSE 8000

# Start backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
