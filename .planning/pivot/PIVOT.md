# Pivot: Better Everyday

**Updated:** 2026-05-10
**Goal:** revive stale side project with minimal bloat.

## Old Product

Eva health chatbot / RAG demo.

Traits:

- Chat-first homepage.
- Hardcoded health categories.
- Browser posts directly to local FastAPI.
- Backend returns/debugs raw model/retrieval output.
- Chroma/model-server flow is interesting but too heavy for first revival slice.

## New Product

Better Everyday: personal source workspace for self-improvement learning.

Core value:

- Capture podcasts, videos, and notes.
- Review before saving.
- Build trustworthy recall from curated sources.
- Use chat as one tool inside the workspace, not the whole product.

## Keep

- Next.js App Router foundation.
- Tailwind styling setup.
- shadcn-style primitives in `src/components/ui/`.
- Python RAG/ingestion code as later reference.
- Existing `.planning/` workflow spine.

## Delete / Sideline First

- Active chat-only homepage.
- `app/components/Proxy.tsx` duplicate.
- `app/api/chat.ts` placeholder/invalid route.
- Any first-slice browser path that calls `http://127.0.0.1:8000/chat`.

## Defer

- Auth.
- Supabase/Postgres/vector storage.
- YouTube automation.
- Production RAG.
- Family accounts.
- Mobile.
- Autonomous agents/coaching.

## First Slice

A static workspace shell:

- Sources panel.
- Paste/transcript ingestion placeholder.
- Notes placeholder.
- Grounded chat placeholder.
- Health, self-help, and AI domain labels.
- Clear empty states.

## Success

Opening the app shows the new product direction without needing backend services.
