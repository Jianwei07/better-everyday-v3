# Technology Stack

**Project:** Better Everyday
**Researched:** 2026-04-22
**Scope:** Target stack for rebuilding the product into a personal-first AI research workspace and adaptive coaching assistant

## Recommended Stack

## Opinionated Recommendation

Rebuild the product as a **Next.js-first TypeScript app on Vercel**, backed by **Supabase Postgres + pgvector**, with **Vercel AI SDK** for chat/tooling and a **small Python ingestion worker** kept off the public request path.

That is the best fit for this exact project because it:

- removes the current brittle browser-to-FastAPI split from the main UX path
- keeps infra mostly free / low-cost
- gives one durable source of truth for chats, memory, sources, chunks, and embeddings
- preserves Python where it is actually useful: transcript ingestion and lightweight local ML utilities
- avoids running heavy local models continuously on a 24 GB laptop

## Core Framework

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| Next.js | 16.x | Web app, server rendering, route handlers, server actions | Official App Router guidance is current and stable; route handlers fix the repo's broken API bridge pattern and let the web app own the public boundary. | HIGH |
| React | 19.x | UI runtime | Current Next.js baseline; good fit for chat UI, streaming, and server/client split. | HIGH |
| TypeScript | 5.x | Full app language | Keep the product surface in one language for UI, app logic, validation, and DB access. | HIGH |
| Vercel AI SDK | 6.x | Chat streaming, provider abstraction, structured outputs, tool calls | Best low-ops fit for a Next.js AI product. It keeps model choice swappable while simplifying streaming chat and narrow agent workflows. | HIGH |
| Zod | 4.x | Request/tool/schema validation | Use one validation model across route handlers, tool inputs, and form parsing. | MEDIUM |

## Database

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| Supabase Postgres | Postgres 17 class managed service | Primary database | One database should hold users, goals, trusted sources, chats, ingestion jobs, chunks, citations, and lightweight memory. This is materially simpler than keeping app state in Postgres and retrieval state in Chroma. | HIGH |
| pgvector | 0.8.x | Vector similarity search | Mature Postgres-native vector search with HNSW/IVFFlat, filtering, hybrid search support, and easy co-location with metadata. Best fit for a personal RAG workspace under low ops constraints. | HIGH |
| Postgres full-text search | Built into Postgres | Lexical retrieval for hybrid search | Personal notes and transcripts benefit from keyword recall. Use hybrid retrieval instead of vector-only search for stronger grounding. | HIGH |
| JSONB + relational tables | Built into Postgres | Metadata, source manifests, memory facts, retrieval diagnostics | Lets you keep flexible metadata without giving up SQL joins and constraints. | HIGH |

## Infrastructure

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| Vercel | Current | Host Next.js app | Cheapest and least-ops path for the web surface; excellent fit for App Router deployments and preview flows. | HIGH |
| Supabase | Current | Managed Postgres, pgvector, optional auth/storage | Best all-in-one free-tier backend for this app shape. Use database first; add Auth/Storage only where needed. | HIGH |
| Python worker / CLI | Python 3.12+ | Transcript fetch, chunking, embedding generation, maintenance scripts | Keep Python for ingestion and offline ML tasks, but do not make it the public app edge. This preserves existing strengths without keeping the current split architecture. | HIGH |
| Optional Inngest | Current | Durable ingestion jobs if async reliability becomes a problem | Good upgrade path for retries and long-running ingestion, but not required on day one for a single-user app. Start simpler. | MEDIUM |

## Recommended Models

| Model | Role | Why it fits this project | Confidence |
|------|------|---------------------------|------------|
| `gemini-2.5-flash` (or current low-cost Flash-class hosted model via AI SDK) | Default answer generation | Best default tradeoff for grounded chat: cheap enough for daily use, strong enough for summarization/tool use, and avoids heating the laptop. Keep it provider-swappable through AI SDK. | MEDIUM |
| `BAAI/bge-small-en-v1.5` | Local embeddings for transcripts/notes | 384-dim embeddings keep storage and compute light. Strong fit for curated English-first knowledge bases on a laptop. | MEDIUM |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | Lightweight reranker | Cheap second-pass reranking improves grounding more reliably than chasing a bigger generation model. Small enough to run on demand locally. | LOW |

### Model policy

- **Default to hosted generation, local retrieval.** This is the right trade for a personal knowledge product.
- **Do not rely on a large always-on local chat model** for v1. It adds heat, latency, and ops overhead without fixing grounding.
- **Spend complexity on retrieval quality first**: chunking, metadata, hybrid search, reranking, and citation display.

## Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Drizzle ORM + drizzle-kit | current | Type-safe schema, migrations, relational access | Use for normal app tables: chats, messages, sources, goals, memories, jobs. |
| `pg` or Neon/Supabase-compatible driver | current | Database transport | Use whatever matches hosting best; keep SQL simple and server-side. |
| `@supabase/supabase-js` | current | Storage and optional auth helpers | Use for file storage or future family accounts; do not make it the only data-access layer. |
| `remark` / `rehype` stack | current | Note/transcript rendering and transforms | Use for sanitized rich source rendering. |
| `youtube-transcript-api` | 1.2.x | Fetch YouTube transcripts without API keys or browsers | First choice for transcript retrieval when subtitles are available. Beware cloud IP blocking. |
| `yt-dlp` | current | Fallback metadata/subtitle extraction | Use as the robust fallback for YouTube ingestion and metadata capture. |
| `tiktoken` or provider tokenizer util | current | Token-aware chunking | Use to keep chunk size stable against the actual model context window. |
| `fastapi` + `pydantic` | 0.128.x / v2 | Private ingestion endpoints only | Use only if the Python worker needs HTTP endpoints; otherwise prefer CLI/offline invocation. |
| `pytest` | 8.x | Ingestion/retrieval tests | Required because current repo has no regression safety net. |
| Vitest + Playwright | current | Web and E2E tests | Needed to protect ingest/chat flows during the rebuild. |

## Recommended System Shape

### 1. Public app path: TypeScript only

Use:

- Next.js pages / layouts / server components for app UI
- Next.js route handlers for `/api/chat`, `/api/ingest`, `/api/search`, `/api/memory`
- Vercel AI SDK for streaming responses and narrow tool use
- Postgres directly from server-side code for memory, retrieval, and persistence

Why: this removes the current hardcoded localhost coupling and creates one production-safe boundary.

### 2. Retrieval: Postgres-native hybrid retrieval

Use this order:

1. metadata filter (`source_type`, `topic`, `trusted`, `date`, `language`)
2. lexical shortlist with Postgres full-text search
3. vector shortlist with pgvector
4. fuse or union results
5. lightweight rerank
6. answer with citation spans back to source chunks

Why: for curated transcripts and notes, hybrid retrieval beats vector-only setups in practice and keeps grounding stronger.

### 3. Ingestion: Python kept as a worker, not the product backbone

Use Python for:

- YouTube transcript fetch
- URL normalization and metadata extraction
- chunking and cleaning
- optional local embedding generation
- offline re-index / repair scripts

Do **not** route normal chat traffic through Python unless a later phase proves it is necessary.

## Prescriptive Choices

### Use this

1. **Next.js + AI SDK as the main app runtime**
   - Best DX and lowest ops for a web-only personal AI app.

2. **Supabase Postgres + pgvector as the single source of truth**
   - Sources, chunks, embeddings, chats, goals, and memory belong together.

3. **Drizzle for schema/migrations, SQL for retrieval-heavy queries**
   - Good balance of safety and control.

4. **Hosted cheap generation + local lightweight embedding/rerank**
   - Best cost/latency/heat trade on this laptop.

5. **Python only for ingestion/offline ML utilities**
   - Reuse existing Python value without keeping split-runtime pain.

### Do not use this

| Avoid | Why |
|------|-----|
| Chroma as the primary long-term store | It duplicates state, complicates deployment, and fights the need for one durable app database. Good prototype tool, wrong default for this rebuild. |
| Browser → FastAPI direct networking | The current repo already shows why this is fragile in production. Put the public boundary in Next route handlers. |
| LangChain-heavy request-path orchestration | Too much abstraction for this app size. Use direct retrieval + AI SDK tools; keep orchestration explicit. |
| Always-on local 7B+ generation | Bad fit for a 24 GB laptop when the product's main problem is grounding, not raw model size. |
| Redis/Celery/Kafka on day one | Overkill for a single-user product. Add durable job infra only after ingestion volume or retry pain justifies it. |
| Prisma as the default ORM | It is viable, but Drizzle is the lighter fit for this stack and keeps SQL/vector work less awkward. |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| App backend | Next.js route handlers | Keep public FastAPI backend | Extra network hop, duplicated contracts, and more deployment friction for a web-only v1 |
| Vector store | pgvector in Postgres | Chroma | Separate persistence layer and weaker fit for app-state + retrieval unification |
| ORM | Drizzle | Prisma | Heavier abstraction layer and less attractive when retrieval logic already wants hand-written SQL |
| Job orchestration | Start simple, add Inngest later if needed | Celery/Redis now | Too much operational weight for single-user ingestion |
| Generation | Hosted low-cost model via AI SDK | Large local model server | More laptop overhead, worse deploy story, little grounding gain |

## Evolution Path From Current Repo

1. **Keep Next.js; rebuild the API boundary in App Router route handlers.**
2. **Move persistence from filesystem Chroma state into Postgres tables + pgvector.**
3. **Shrink FastAPI into a private ingestion utility layer or remove it from the hot path entirely.**
4. **Replace LangChain-centric request orchestration with explicit retrieval + AI SDK tools.**
5. **Add hybrid retrieval and citations before adding broader coaching behaviors.**
6. **Only add durable background job infrastructure if real ingestion failure modes demand it.**

## Minimal Schema Direction

Use Postgres tables roughly like:

- `sources`
- `source_revisions`
- `chunks`
- `chat_threads`
- `chat_messages`
- `goals`
- `trusted_sources`
- `memory_items`
- `ingestion_jobs`
- `retrieval_feedback`

Why: this supports both grounded recall and adaptive coaching without inventing a separate "memory system" too early.

## Installation

```bash
# app
npm install next react react-dom ai zod drizzle-orm @supabase/supabase-js
npm install -D typescript vitest playwright drizzle-kit

# optional db driver (pick one deployment-aligned path)
npm install pg

# python ingestion worker
uv add fastapi pydantic youtube-transcript-api yt-dlp sentence-transformers pgvector psycopg[binary] pytest
```

## Confidence Notes

- **HIGH:** Next.js App Router route handlers, AI SDK fit, Supabase/Postgres/pgvector unification, and keeping Python off the public request path are all directly supported by current docs and strongly aligned with the repo's current failure modes.
- **MEDIUM:** Drizzle-over-Prisma and hosted-Flash-model-as-default are architecture recommendations with good ecosystem support, but they remain opinionated choices.
- **LOW:** Specific small local reranker model choice should be validated against the actual transcript corpus during implementation.

## Sources

- Next.js route handlers docs (v16.2.4, updated 2026-04-21): https://nextjs.org/docs/app/api-reference/file-conventions/route
- Vercel AI SDK docs: https://ai-sdk.dev/docs/introduction
- Vercel AI SDK RAG/tool examples via Context7: `/vercel/ai`
- FastAPI background tasks docs: https://fastapi.tiangolo.com/tutorial/background-tasks/
- Supabase pgvector docs: https://supabase.com/docs/guides/database/extensions/pgvector
- Supabase pgvector / semantic search examples via Context7: `/supabase/supabase`
- pgvector README / indexing + filtering guidance: https://github.com/pgvector/pgvector
- Drizzle ORM docs via Context7: `/drizzle-team/drizzle-orm-docs`
- Prisma docs via Context7: `/prisma/prisma`
- YouTube Transcript API README / release info: https://github.com/jdepoix/youtube-transcript-api
- yt-dlp README: https://github.com/yt-dlp/yt-dlp
