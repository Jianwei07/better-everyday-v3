# Integrations Map

**Updated:** 2026-05-10

## Current Integrations

- Browser -> FastAPI direct call exists in legacy `app/components/Chatbot.tsx`.
- Browser -> FastAPI direct call also exists in duplicate `app/components/Proxy.tsx`.
- Placeholder server call exists in `app/api/chat.ts` to `https://your-aws-lambda-url/chat`.
- Next rewrites exist in `next.config.js` for `/api/py/:path*`, `/docs`, and `/openapi.json`.
- Backend -> model server call exists in `api/chat.py` through `LLM_SERVER_URL`.
- Backend -> Chroma exists through `api/config.py`, `api/embedding_search.py`, and `api/add_data.py`.
- Docker Compose defines local FastAPI/model-server style development.

## Env Names Seen

- `FASTAPI_DEV_URL`
- `FASTAPI_PROD_URL`
- `LLM_SERVER_URL`
- `EMBEDDING_MODEL_NAME`
- `HUGGINGFACE_HUB_TOKEN_WRITE`
- `IS_DOCKER`

## First-Slice Integration Policy

- No active backend dependency.
- No user-triggered network call to localhost.
- No production model server or vector DB needed.
- Chat appears as a placeholder until approved sources and a safe boundary exist.

## Later Integration Direction

- Add a Next.js BFF/API route before restoring browser chat.
- Gate backend debug endpoints before public use.
- Move durable app state to a real store when ingestion becomes real.
- Keep Python for ingestion/offline ML utilities unless a backend API is explicitly needed.
