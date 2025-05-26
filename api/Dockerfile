# Use official slim Python image for smaller base
FROM python:3.10-slim

# Set environment variables
ENV CHROMA_PATH=/chroma_storage \
    EMBEDDING_MODEL_NAME=default-embedding-model \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /api

# Install build tools only if necessary (uncomment if you need them)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only code (after dependencies to maximize cache use)
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
