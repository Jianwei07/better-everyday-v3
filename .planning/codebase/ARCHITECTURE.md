# Architecture

**Analysis Date:** 2026-04-21

## Pattern Overview

**Overall:** Split frontend/backend application with a thin Next.js UI layer and a Python RAG service layer.

**Key Characteristics:**
- The web UI in `app/page.tsx` and `app/components/Chatbot.tsx` owns interaction state and calls the backend over HTTP.
- The backend in `api/main.py`, `api/api.py`, and `api/chat.py` keeps HTTP routing separate from retrieval and prompt orchestration.
- Retrieval is organized around topic-specific Chroma collections managed through `api/add_data.py`, `api/embedding_search.py`, and `api/config.py`.

## Layers

**Web App Layer:**
- Purpose: Render the chat experience and collect user input.
- Location: `app/`
- Contains: App Router entry files in `app/page.tsx` and `app/layout.tsx`, plus the main interactive client component in `app/components/Chatbot.tsx`.
- Depends on: React state/hooks, Next.js dynamic import in `app/page.tsx`, and shared UI primitives from `src/components/ui/*`.
- Used by: Browser clients visiting the Next.js app.

**Shared UI Primitive Layer:**
- Purpose: Provide reusable presentational building blocks for the web app.
- Location: `src/components/ui/` and `src/lib/utils.ts`
- Contains: Shadcn-style primitives such as `src/components/ui/button.tsx`, `src/components/ui/card.tsx`, `src/components/ui/input.tsx`, and class merging helper `src/lib/utils.ts`.
- Depends on: Radix UI packages and utility helpers configured through `components.json` and `tsconfig.json`.
- Used by: `app/components/Chatbot.tsx` and `app/components/Proxy.tsx`.

**HTTP API Layer:**
- Purpose: Expose backend routes and app lifecycle configuration.
- Location: `api/main.py` and `api/api.py`
- Contains: FastAPI app creation, CORS middleware, router registration, request models, and `/chat` plus `/test_llm` endpoints.
- Depends on: FastAPI, Pydantic, `api/chat.py`, and `api/utils.py`.
- Used by: The frontend fetch in `app/components/Chatbot.tsx` and local/manual callers described in `README-backend.md`.

**RAG Orchestration Layer:**
- Purpose: Turn a user question into a grounded answer.
- Location: `api/chat.py`
- Contains: Prompt template definition, async LLM HTTP client, generic-answer detection, optional self-reflection pass, and final output shaping.
- Depends on: `api/embedding_search.py` for retrieval, `api/config.py` for `LLM_SERVER_URL`, and `api/utils.py` for output cleanup.
- Used by: `/chat` in `api/api.py`.

**Vector Retrieval and Ingestion Layer:**
- Purpose: Build and query topic-scoped knowledge stores.
- Location: `api/add_data.py`, `api/embedding_search.py`, `api/config.py`, and `chroma_storage/`
- Contains: Markdown loading from `data/`, chunking, metadata tagging, Chroma persistence, and query-time embedding search.
- Depends on: LangChain loaders/splitters, Hugging Face embeddings, ChromaDB, and markdown source files such as `data/neuro/neuro.md`.
- Used by: CLI ingestion via `api/add_data.py` and request-time retrieval via `api/chat.py`.

## Data Flow

**Interactive chat request:**

1. `app/page.tsx` dynamically loads `app/components/Chatbot.tsx` with `ssr: false`, so the chat UI runs entirely on the client.
2. `app/components/Chatbot.tsx` stores `chatHistory`, `selectedTopic`, and input state, then POSTs `{ message, topic }` to `http://127.0.0.1:8000/chat`.
3. `api/api.py` validates the payload with `ChatRequest` and calls `generate_response_with_context()` from `api/chat.py`.
4. `api/chat.py` asks `api/embedding_search.py` for context from the topic-named Chroma collection, formats the RAG prompt, then calls the external LLM server URL from `api/config.py`.
5. `api/utils.py` normalizes the LLM output into `cleaned_text`, `answer_blocks`, and `raw`, and `api/api.py` returns that JSON to the frontend.
6. `app/components/Chatbot.tsx` removes the temporary typing message and appends the returned answer to `chatHistory`.

**Data ingestion flow:**

1. `api/add_data.py` loads markdown documents from a source folder such as `data/neuro/`.
2. `api/add_data.py` splits documents into chunks and stamps each chunk with a lowercase `category` metadata field.
3. `api/add_data.py` writes chunks into a Chroma collection whose name matches the category.
4. `api/embedding_search.py` later reuses that category name to open the same collection during retrieval.

**State Management:**
- Frontend state is local component state in `app/components/Chatbot.tsx`; there is no shared client store.
- Backend request state is stateless per request, with shared process-level resources initialized in `api/config.py` and `api/embedding_search.py`.

## Key Abstractions

**Topic-scoped collection:**
- Purpose: Isolate retrieval data by health domain.
- Examples: `api/add_data.py`, `api/embedding_search.py`, `chroma_storage/`
- Pattern: The collection name and metadata filter both derive from the normalized topic/category string.

**Chat request model:**
- Purpose: Define the public contract for chat calls.
- Examples: `api/api.py`
- Pattern: Pydantic request models (`ChatRequest`, `TestRequest`) validate incoming JSON before business logic runs.

**Output cleaning wrapper:**
- Purpose: Convert inconsistent LLM output into a frontend-safe response shape.
- Examples: `api/utils.py`, `api/api.py`, `api/chat.py`
- Pattern: All final backend responses pass through `extract_eva_response()` before returning to clients.

**Client-only chatbot shell:**
- Purpose: Contain all browser-only behavior away from server-rendered layout code.
- Examples: `app/page.tsx`, `app/components/Chatbot.tsx`
- Pattern: `dynamic(() => import("./components/Chatbot"), { ssr: false })` keeps the interactive chat widget off the server render path.

## Entry Points

**Next.js page entry:**
- Location: `app/page.tsx`
- Triggers: Requests to the site root.
- Responsibilities: Render the page shell and mount the client-only chatbot.

**Next.js layout entry:**
- Location: `app/layout.tsx`
- Triggers: Every App Router page render.
- Responsibilities: Load global CSS, register local fonts, and wrap page content.

**FastAPI app entry:**
- Location: `api/main.py`
- Triggers: `uvicorn api.main:app --reload`, container startup, or Lambda-style hosting through `handler = Mangum(app)`.
- Responsibilities: Construct the FastAPI app, apply CORS, and attach the router.

**Backend route entry:**
- Location: `api/api.py`
- Triggers: POSTs to `/chat` and `/test_llm`.
- Responsibilities: Validate requests, call orchestration code, and shape JSON responses.

**Ingestion CLI entry:**
- Location: `api/add_data.py`
- Triggers: Manual ingestion commands.
- Responsibilities: Load source docs, split them, and persist them into Chroma.

## Error Handling

**Strategy:** Fail soft with fallback strings and broad exception handling instead of propagating detailed errors to the UI.

**Patterns:**
- `api/chat.py` wraps LLM calls and orchestration in `try/except`, returning user-readable fallback answers on timeout or failure.
- `api/api.py` converts unexpected backend failures into HTTP 500 responses with `HTTPException`.
- `app/components/Chatbot.tsx` catches fetch failures and appends a generic error message to chat history.

## Cross-Cutting Concerns

**Logging:** `api/main.py`, `api/chat.py`, `api/api.py`, `api/embedding_search.py`, and `api/utils.py` rely on `logging.basicConfig(...)` plus many `print(...)` debug statements.
**Validation:** Request payloads are validated with Pydantic in `api/api.py`; topic normalization is reinforced in `api/add_data.py` and `api/embedding_search.py` via lowercase trimming.
**Authentication:** Not detected in `app/` or `api/`; the backend endpoints in `api/api.py` are open apart from CORS restrictions in `api/main.py`.

---

*Architecture analysis: 2026-04-21*
