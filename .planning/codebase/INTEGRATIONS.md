# External Integrations

**Analysis Date:** 2026-04-21

## APIs & External Services

**Frontend → Backend HTTP:**
- FastAPI chat API - primary application API used by the UI for chat responses.
  - SDK/Client: browser `fetch` in `app/components/Chatbot.tsx` and `app/components/Proxy.tsx`
  - Auth: Not detected
- Next.js rewrite proxy - maps frontend `/api/py/:path*`, `/docs`, and `/openapi.json` requests to the FastAPI base URL.
  - SDK/Client: `next.config.js`
  - Auth: `FASTAPI_DEV_URL`, `FASTAPI_PROD_URL`

**LLM Inference:**
- llama.cpp server - backend sends prompt-completion requests to a separate inference service from `api/chat.py`; local compose wiring exposes it as `eva-llama-cpp` in `docker-compose.yml`.
  - SDK/Client: `httpx` in `api/chat.py`
  - Auth: `LLM_SERVER_URL`
- AWS Lambda endpoint (placeholder path) - legacy/prototype proxy route posts to `https://your-aws-lambda-url/chat` in `app/api/chat.ts`.
  - SDK/Client: server-side `fetch` in `app/api/chat.ts`
  - Auth: Not detected

**Model Distribution:**
- Hugging Face Hub - model download/cache management is implied by `huggingface-hub`, `sentence-transformers`, and `transformers` in `requirements.txt`; explicit cache deletion is scripted in `api/remove_model.py`.
  - SDK/Client: `huggingface_hub`, `sentence-transformers`, `transformers`
  - Auth: `HUGGINGFACE_HUB_TOKEN_WRITE`

## Data Storage

**Databases:**
- ChromaDB persistent local vector store - embeddings and retrieved document chunks are stored on disk.
  - Connection: `CHROMA_PATH` behavior is set in `api/config.py`; `IS_DOCKER=true` switches storage to `/chroma_storage`
  - Client: `chromadb.PersistentClient` in `api/config.py`, plus LangChain `Chroma` in `api/add_data.py`

**File Storage:**
- Local filesystem only - source documents are loaded from folders such as `data/neuro` via `api/add_data.py`; vector storage persists under `./chroma_storage` or `/chroma_storage` via `api/config.py` and `docker-compose.yml`.

**Caching:**
- Hugging Face local model cache - used implicitly by `sentence-transformers` / `transformers`, with cleanup utility in `api/remove_model.py`.

## Authentication & Identity

**Auth Provider:**
- Custom / none - no user auth provider, session library, or identity middleware was detected in `app/`, `src/`, or `api/`.
  - Implementation: unauthenticated chat requests to `/chat` in `api/api.py`

## Monitoring & Observability

**Error Tracking:**
- None detected - no Sentry, Bugsnag, Datadog, or similar client/server SDKs were found.

**Logs:**
- Standard logging and prints - `logging.basicConfig(level=logging.INFO)` is set in `api/main.py`, while request/debug/error output is emitted with `print()` across `api/api.py`, `api/chat.py`, `api/add_data.py`, and `api/embedding_search.py`.

## CI/CD & Deployment

**Hosting:**
- Vercel - frontend deployment is configured in `vercel.json`.
- Docker Compose - documented local runtime for `fastapi-backend` and `llm-server` in `docker-compose.yml`.
- AWS Lambda compatible path - backend adapter exists in `api/main.py` via `Mangum`.

**CI Pipeline:**
- None detected - no `.github/workflows/*` files were found.

## Environment Configuration

**Required env vars:**
- `FASTAPI_DEV_URL` - frontend rewrite target in `next.config.js`
- `FASTAPI_PROD_URL` - production rewrite target in `next.config.js`
- `HUGGINGFACE_HUB_TOKEN_WRITE` - backend Hugging Face token in `api/config.py`
- `EMBEDDING_MODEL_NAME` - embedding model selector in `api/config.py`
- `LLM_SERVER_URL` - inference server endpoint in `api/config.py`
- `IS_DOCKER` - storage mode switch in `api/config.py` and `docker-compose.yml`

**Secrets location:**
- `.env.local` is referenced by `docker-compose.yml` as the local env file.
- Frontend runtime env is read directly from host environment in `next.config.js`.

## Webhooks & Callbacks

**Incoming:**
- `POST /chat` in `api/api.py`
- `POST /test_llm` in `api/api.py`
- `/api/py/:path*`, `/docs`, and `/openapi.json` rewrites in `next.config.js`

**Outgoing:**
- Backend POSTs to `LLM_SERVER_URL` from `api/chat.py`
- Frontend POSTs to `http://127.0.0.1:8000/chat` from `app/components/Chatbot.tsx` and `app/components/Proxy.tsx`
- Placeholder server route POSTs to `https://your-aws-lambda-url/chat` from `app/api/chat.ts`

---

*Integration audit: 2026-04-21*
