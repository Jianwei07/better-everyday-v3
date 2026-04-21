# Codebase Structure

**Analysis Date:** 2026-04-21

## Directory Layout

```text
better-everyday-v3/
├── app/                    # Next.js App Router pages and client chat components
├── api/                    # FastAPI backend, RAG logic, and ingestion scripts
├── src/                    # Shared frontend UI primitives and utilities
├── data/                   # Source markdown content for ingestion
├── chroma_storage/         # Persistent local Chroma vector store files
├── public/                 # Static assets served by Next.js
├── image/                  # Extra image assets referenced by the frontend
├── .planning/codebase/     # Generated codebase mapping documents
├── package.json            # Frontend package manifest
├── tsconfig.json           # TypeScript config and path aliases
├── next.config.js          # Next.js rewrites to backend endpoints
├── docker-compose.yml      # Local multi-service orchestration
└── vercel.json             # Vercel deployment configuration for the frontend
```

## Directory Purposes

**`app/`:**
- Purpose: Hold the Next.js App Router surface.
- Contains: `app/page.tsx`, `app/layout.tsx`, `app/globals.css`, `app/components/Chatbot.tsx`, and `app/api/chat.ts`.
- Key files: `app/page.tsx`, `app/layout.tsx`, `app/components/Chatbot.tsx`

**`app/components/`:**
- Purpose: Store feature-level client components that are specific to the chat UI.
- Contains: `app/components/Chatbot.tsx` and `app/components/Proxy.tsx`.
- Key files: `app/components/Chatbot.tsx`, `app/components/Proxy.tsx`

**`src/components/ui/`:**
- Purpose: Store reusable presentational primitives shared by feature components.
- Contains: `src/components/ui/avatar.tsx`, `src/components/ui/button.tsx`, `src/components/ui/card.tsx`, `src/components/ui/input.tsx`.
- Key files: `src/components/ui/button.tsx`, `src/components/ui/card.tsx`

**`src/lib/`:**
- Purpose: Hold shared frontend helpers.
- Contains: Utility helpers such as `src/lib/utils.ts`.
- Key files: `src/lib/utils.ts`

**`api/`:**
- Purpose: Hold the Python backend package and local maintenance scripts.
- Contains: FastAPI setup in `api/main.py`, routes in `api/api.py`, orchestration in `api/chat.py`, retrieval in `api/embedding_search.py`, ingestion in `api/add_data.py`, and helper/debug scripts.
- Key files: `api/main.py`, `api/api.py`, `api/chat.py`, `api/embedding_search.py`, `api/add_data.py`, `api/config.py`

**`data/`:**
- Purpose: Hold raw markdown knowledge sources for ingestion.
- Contains: Category folders such as `data/neuro/`.
- Key files: `data/neuro/neuro.md`

**`chroma_storage/`:**
- Purpose: Persist local vector data outside application code.
- Contains: Chroma SQLite and binary index files.
- Key files: `chroma_storage/chroma.sqlite3`

**`public/`:**
- Purpose: Hold standard Next.js static assets.
- Contains: `public/next.svg`, `public/vercel.svg`.
- Key files: `public/next.svg`, `public/vercel.svg`

**`image/`:**
- Purpose: Hold extra image assets used by the chat UI.
- Contains: `image/chatbot-avatar-v1.png`.
- Key files: `image/chatbot-avatar-v1.png`

## Key File Locations

**Entry Points:**
- `app/page.tsx`: Root page that mounts the chatbot UI.
- `app/layout.tsx`: Global page wrapper and font setup.
- `api/main.py`: FastAPI startup entry used by uvicorn and optional Lambda hosting.
- `api/add_data.py`: CLI entry for vector ingestion.

**Configuration:**
- `package.json`: Frontend scripts and JS dependencies.
- `tsconfig.json`: TypeScript settings and `@/*` alias mapping to `src/*`.
- `next.config.js`: Development/production rewrites for backend routes.
- `vercel.json`: Vercel build and route behavior.
- `api/config.py`: Backend environment-variable driven runtime settings.

**Core Logic:**
- `app/components/Chatbot.tsx`: Main frontend feature implementation.
- `api/api.py`: HTTP contract for chat endpoints.
- `api/chat.py`: Prompting, LLM calls, and response pipeline.
- `api/embedding_search.py`: Chroma retrieval by topic.
- `api/utils.py`: LLM output cleanup and response shaping.

**Testing:**
- `api/test.py`: Manual Chroma inspection script, not an automated test suite.
- `api/check_data.py`: Data inspection/debugging helper for Chroma contents.

## Naming Conventions

**Files:**
- Next.js route files use framework names: `app/page.tsx`, `app/layout.tsx`.
- Frontend feature and UI component files use PascalCase or component-style names: `app/components/Chatbot.tsx`, `src/components/ui/Button` pattern represented by `button.tsx`.
- Python backend modules use snake_case: `api/embedding_search.py`, `api/add_data.py`, `api/chroma_db_checker.py`.

**Directories:**
- Frontend route directories follow Next.js conventions: `app/`, `app/components/`, `app/api/`.
- Python/backend and data directories are lowercase nouns: `api/`, `data/`, `public/`, `image/`, `chroma_storage/`.

## Where to Add New Code

**New Feature:**
- Primary code: Add new page-level UI to `app/` and new chat-specific components beside `app/components/Chatbot.tsx` when the feature is user-facing.
- Tests: Not applicable; no automated frontend or backend test directory is present.

**New Component/Module:**
- Implementation: Put reusable frontend primitives in `src/components/ui/`; put feature-specific chat UI in `app/components/`; put new backend route handlers in `api/api.py` and supporting backend modules in `api/`.

**Utilities:**
- Shared helpers: Put frontend helpers in `src/lib/` and backend helpers in `api/utils.py` or a new sibling utility module under `api/`.

## Special Directories

**`.planning/codebase/`:**
- Purpose: Stores generated reference documents for other GSD commands.
- Generated: Yes
- Committed: Yes

**`chroma_storage/`:**
- Purpose: Stores persistent vector database state created by ingestion and retrieval workflows.
- Generated: Yes
- Committed: Yes

**`app/api/`:**
- Purpose: Intended location for Next.js-side API handlers; current contents are `app/api/chat.ts`.
- Generated: No
- Committed: Yes

**`api/__pycache__/`:**
- Purpose: Stores Python bytecode cache files.
- Generated: Yes
- Committed: Yes

## Placement Guidance

- Put new root pages under `app/<route>/page.tsx` or `app/page.tsx`-adjacent route folders, not under `src/`.
- Keep shared visual primitives under `src/components/ui/` so `@/components/ui/*` imports continue to resolve through `tsconfig.json`.
- Keep backend HTTP surface area thin by extending `api/api.py` for request/response contracts and moving new business logic into dedicated modules under `api/`.
- Add new ingestible knowledge sources under `data/<category>/` and use the matching lowercase category when updating `api/add_data.py` workflows.
- Treat `app/components/Proxy.tsx`, `app/api/chat.ts`, and debug scripts such as `api/check_data.py` as peripheral files; extend `app/components/Chatbot.tsx`, `api/api.py`, and `api/chat.py` first when changing the active request path.

---

*Structure analysis: 2026-04-21*
