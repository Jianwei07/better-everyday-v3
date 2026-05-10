# Architecture Map

**Updated:** 2026-05-10

## Current Shape

Better Everyday is a brownfield split app:

- `app/`: Next.js browser surface.
- `src/components/ui/`: reusable UI primitives.
- `api/`: FastAPI backend for chat/RAG.
- `data/`: markdown source material.
- `chroma_storage/`: committed local vector store artifacts.

## Active Product Seam

Phase 1 should use the browser/UI seam only:

- User opens `app/page.tsx`.
- Page shows a workspace shell: sources, ingest, notes, chat placeholder.
- No first-slice browser action should call `http://127.0.0.1:8000/chat`.

## Legacy Chat Flow

Legacy flow still exists as dormant/debt code:

1. `app/components/Chatbot.tsx` owns chat state and topic UI.
2. It posts directly to `http://127.0.0.1:8000/chat`.
3. FastAPI route in `api/api.py` calls `api/chat.py`.
4. `api/chat.py` retrieves from Chroma and calls a model server.
5. Response is cleaned by `api/utils.py`.

## Module / Interface Notes

- Module: `app/page.tsx` should become the product shell module.
- Module: `app/components/Chatbot.tsx` is legacy implementation, not first-slice product core.
- Interface: future web-to-backend boundary should be a Next route/BFF or explicit API adapter, not browser-to-FastAPI direct calls.
- Seam: ingestion should start as UI + review model, then backend persistence later.
- Adapter: Python backend should become ingestion/offline ML utility first, not public browser boundary.

## Depth / Locality

- Deep slice: one clear workspace shell that proves product direction.
- Shallow/bloat risk: preserving old chatbot and adding new features around it.
- Locality goal: first changes should stay in `app/page.tsx`, `app/layout.tsx`, and small planning docs.

## Architecture Rule For First Slice

Do not wire production RAG yet. Prove the product shape and remove active localhost coupling first.
