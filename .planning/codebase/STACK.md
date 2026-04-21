# Technology Stack

**Analysis Date:** 2026-04-21

## Languages

**Primary:**
- TypeScript / TSX - frontend app code in `app/page.tsx`, `app/layout.tsx`, `app/components/Chatbot.tsx`, `src/components/ui/*.tsx`, and `src/lib/utils.ts`.
- Python - backend API, retrieval, ingestion, and model utilities in `api/main.py`, `api/api.py`, `api/chat.py`, `api/add_data.py`, `api/embedding_search.py`, and related scripts under `api/`.

**Secondary:**
- JavaScript (CommonJS config) - framework and build configuration in `next.config.js`, `tailwind.config.js`, and `postcss.config.js`.
- YAML - container orchestration in `docker-compose.yml` and package locking in `pnpm-lock.yaml`.

## Runtime

**Environment:**
- Node.js - required by `next` and `react` in `package.json`; exact Node version is not pinned in-repo.
- Python 3.12 (containerized) - backend image uses `python:3.12-slim` in `api/Dockerfile`.

**Package Manager:**
- npm - primary frontend script runner via `package.json` and `package-lock.json`.
- pnpm lockfile also present in `pnpm-lock.yaml`, so JS dependency state exists for both npm and pnpm.
- Python dependencies install through `uv pip install -r requirements.txt` in `api/Dockerfile` and `README-backend.md`.
- Lockfile: present in `package-lock.json`; additional JS lockfile present in `pnpm-lock.yaml`.

## Frameworks

**Core:**
- Next.js `^15.3.2` - React frontend and routing in `package.json`, `app/page.tsx`, `app/layout.tsx`, and `next.config.js`.
- React `^19.1.0` - client UI and stateful chat interface in `package.json` and `app/components/Chatbot.tsx`.
- FastAPI `0.115.9` - backend HTTP API in `requirements.txt`, `api/main.py`, and `api/api.py`.
- LangChain `0.3.25` family - prompt orchestration and ingestion helpers in `requirements.txt`, `api/chat.py`, and `api/add_data.py`.
- ChromaDB `1.0.13` - persistent vector store in `requirements.txt`, `api/config.py`, and `api/embedding_search.py`.

**Testing:**
- Not detected. No Jest, Vitest, pytest, or similar test config files were found at the repository root.

**Build/Dev:**
- Tailwind CSS `^3.4.14` - styling system configured in `package.json`, `tailwind.config.js`, and `app/globals.css`.
- PostCSS `^8.4.47` with Autoprefixer `^10.4.20` - CSS processing in `postcss.config.js`.
- ESLint `^8.57.1` with `eslint-config-next` `15.0.1` - frontend linting via `.eslintrc.json` and `package.json`.
- Docker Compose - local multi-service development in `docker-compose.yml`.
- Uvicorn `0.32.0` - Python ASGI server in `requirements.txt` and `api/main.py`.
- Mangum `0.19.0` - optional AWS Lambda adapter in `requirements.txt` and `api/main.py`.

## Key Dependencies

**Critical:**
- `next` - frontend runtime and route handling for the app in `package.json` and `app/`.
- `react` / `react-dom` - chat UI rendering in `package.json` and `app/components/Chatbot.tsx`.
- `fastapi` - backend request handling in `requirements.txt` and `api/api.py`.
- `httpx` - async HTTP client used to call the LLM server from `api/chat.py`.
- `langchain-core`, `langchain-community`, `langchain-chroma`, `langchain-huggingface` - retrieval and ingestion plumbing in `requirements.txt` and `api/add_data.py`.
- `chromadb` - local persistent embeddings store in `requirements.txt`, `api/config.py`, and `api/embedding_search.py`.
- `sentence-transformers`, `transformers`, `torch` - embedding generation and reranking in `requirements.txt`, `api/embedding_search.py`, and `api/rerank.py`.

**Infrastructure:**
- `mangum` - optional Lambda packaging path for `api/main.py`.
- `python-dotenv` - environment loading support is installed via `requirements.txt`.
- `@radix-ui/react-avatar`, `@radix-ui/react-slot`, `class-variance-authority`, `clsx`, `tailwind-merge`, `tailwindcss-animate`, `lucide-react` - UI system dependencies used by `src/components/ui/*.tsx`, `src/lib/utils.ts`, and `app/components/Chatbot.tsx`.

## Configuration

**Environment:**
- Frontend-to-backend routing is configured with `FASTAPI_DEV_URL` and `FASTAPI_PROD_URL` in `next.config.js`.
- Backend model and storage settings are configured with `HUGGINGFACE_HUB_TOKEN_WRITE`, `EMBEDDING_MODEL_NAME`, `LLM_SERVER_URL`, and `IS_DOCKER` in `api/config.py`.
- Docker-local environment injection references `.env.local` via `docker-compose.yml` without committing the file contents.

**Build:**
- Next.js config: `next.config.js`
- TypeScript config: `tsconfig.json`
- Vercel deployment config: `vercel.json`
- Tailwind config: `tailwind.config.js`
- PostCSS config: `postcss.config.js`
- ESLint config: `.eslintrc.json`
- Backend container build: `api/Dockerfile`
- Local orchestration: `docker-compose.yml`

## Platform Requirements

**Development:**
- Node.js plus npm-compatible tooling for the frontend in `package.json`.
- Python dependencies for backend scripts in `requirements.txt` and `api/requirements.txt`.
- Docker / Docker Compose for the repo's documented local stack in `docker-compose.yml`, `README.md`, and `README-backend.md`.
- Local model assets mounted from `./models` for the `llm-server` service in `docker-compose.yml`.
- Local persistent data directories `./chroma_storage` and `./data` for retrieval storage and source documents in `docker-compose.yml` and `api/add_data.py`.

**Production:**
- Vercel-hosted Next.js frontend defined by `vercel.json`.
- FastAPI backend reachable through `FASTAPI_PROD_URL` rewrites in `next.config.js`.
- Optional AWS Lambda-compatible backend packaging via `Mangum` in `api/main.py`.

---

*Stack analysis: 2026-04-21*
