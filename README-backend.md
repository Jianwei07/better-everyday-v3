# Eva Health Chatbot Backend (RAG)

## Overview

This backend uses FastAPI, ChromaDB, and a local LLM server (e.g., TGI, llama.cpp, vLLM) for efficient Retrieval-Augmented Generation (RAG) health advice.

## Quick Start (Local)

1. **Clone repo and install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare vector DB:**

   ```bash
   python api/add_data.py
   ```

3. **Start LLM server (TGI example):**

   ```bash
   bash api/llm_server_example.sh
   # Or use Docker Compose: docker compose up llm-server
   ```

   - For llama.cpp or vLLM, see their docs and set `LLM_SERVER_URL` in `.env.local` accordingly.

4. **Start FastAPI backend:**

   ```bash
   uvicorn api.main:app --reload
   # Or with Docker Compose: docker compose up fastapi-backend
   ```

5. **Frontend:**
   - The Next.js frontend connects to FastAPI at `localhost:8000`.

## Environment Variables (`.env.local`)

```
CHROMA_PATH=./chroma_storage
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
LLM_SERVER_URL=http://localhost:8001/v1/completions
```

## Docker Compose

- `docker-compose.yml` orchestrates FastAPI, LLM server, and persistent ChromaDB storage.
- For changes in programs

  - docker compose build
  - If You Change Dockerfile or requirements.txt: docker-compose up --build

- To run all services:
  ```bash
  docker compose up
  Check container status	docker-compose ps
  Check logs	            docker-compose logs -f fastapi-backend
  ```
  curl -X POST http://localhost:8000/chat \
   -H "Content-Type: application/json" \
   -d '{"message": "How do I improve my brain health?", "topic": "Neuro"}'

## Notes

- The backend now calls the LLM server via HTTP for generation (no in-process model loading).
- All services use the same `CHROMA_PATH` for vector DB.
- For production, use a GPU for the LLM server and secure your endpoints.

## Troubleshooting

- If you see LLM timeout errors, check that the LLM server is running and accessible at `LLM_SERVER_URL`.
- To change the model, update the LLM server launch command and `.env.local`.
