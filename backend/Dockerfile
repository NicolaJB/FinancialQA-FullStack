FROM python:3.11-slim AS base
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential git curl bash \
    && rm -rf /var/lib/apt/lists/*

FROM base
WORKDIR /app/backend

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
