FROM python:3.12-slim

WORKDIR /api_embedder

ENV MODEL=jinaai/jina-embeddings-v3 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/api_embedder/cache_models

COPY requirements.txt .
 
RUN mkdir cache_models inputs logs outputs

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
