# Technology Stack

**Updated:** 2026-05-10

## Runtime

- Frontend: Next.js App Router in `app/`.
- UI: React + TypeScript + Tailwind CSS.
- Shared UI primitives: shadcn-style components in `src/components/ui/`.
- Backend: FastAPI/Python in `api/`.
- Retrieval: Chroma local vector store in `chroma_storage/` plus source markdown in `data/`.
- Inference: local/model-server style HTTP call from `api/chat.py` using `LLM_SERVER_URL`.

## Current Package State

- `package.json` uses `next`, `react`, `react-dom`, `lucide-react`, Tailwind, and Radix primitives.
- Both `package-lock.json` and `pnpm-lock.yaml` exist; prefer `npm` unless the project decides otherwise.
- `requirements.txt` and `api/requirements.txt` both exist; backend dependency source is split.
- `next.config.js` defines FastAPI rewrites, but legacy chat components still hardcode localhost.

## Frontend Commands

- Dev: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`

## Backend Commands

- Docker path exists through `docker-compose.yml`.
- Backend entrypoint: `uvicorn api.main:app --reload` once imports/config are healthy.
- Ingestion reference: `python api/add_data.py --data_path data/neuro --category neuro --chunk_size 300 --chunk_overlap 100`.

## Stack Direction

- Phase 1 should stay frontend-only.
- Do not depend on FastAPI, Chroma, model server, Supabase, auth, or hosted inference for the first slice.
- Later direction can move toward Next.js BFF + durable Postgres/vector storage, but not in this slice.
