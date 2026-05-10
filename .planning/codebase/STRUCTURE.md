# Structure Map

**Updated:** 2026-05-10

## Top Level

```text
better-everyday-v3/
  app/                 Next.js App Router UI
  api/                 FastAPI/RAG backend and scripts
  src/components/ui/   shared UI primitives
  src/lib/             frontend utilities
  data/                source markdown
  chroma_storage/      generated local vector store artifacts
  .planning/           project-local Jayden Workflow state
```

## Important Frontend Files

- `app/page.tsx`: current homepage / workspace shell target.
- `app/layout.tsx`: metadata, fonts, global wrapper.
- `app/globals.css`: global styling.
- `app/components/Chatbot.tsx`: legacy client chatbot, large and stateful.
- `app/components/Proxy.tsx`: duplicate legacy chatbot, should not be active.
- `app/api/chat.ts`: invalid/stale App Router API file.

## Important Backend Files

- `api/main.py`: FastAPI app startup.
- `api/api.py`: HTTP routes for chat/debug.
- `api/chat.py`: RAG prompt, retrieval call, LLM server call.
- `api/embedding_search.py`: Chroma retrieval.
- `api/add_data.py`: ingestion script.
- `api/config.py`: backend env/config.

## Where New Code Should Go

- Phase 1 workspace UI: `app/page.tsx` only if possible.
- Product metadata: `app/layout.tsx`.
- Shared UI primitives: `src/components/ui/` only if a reusable primitive is actually needed.
- Backend changes: defer until a later phase.
- Tests: add only when behavior becomes executable; first slice can rely on build/static checks.

## Where Not To Add Code Yet

- Do not add a copied skills harness into this repo.
- Do not add a new backend API during first slice.
- Do not expand `Chatbot.tsx`; it is legacy debt.
- Do not add Supabase/auth/mobile/family-account structure yet.
