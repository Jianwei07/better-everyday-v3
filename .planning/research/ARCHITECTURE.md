# Architecture Patterns

**Domain:** Personal AI research workspace
**Researched:** 2026-04-22
**Overall confidence:** HIGH

## Recommended Architecture

Rebuild this as a **four-layer system** with a clear web boundary, an application/service boundary, an asynchronous ingestion pipeline, and a single persistent data layer.

```text
Browser
  ↓
Next.js web app
  - UI routes
  - Server Actions / Route Handlers as BFF
  - auth/session, request validation, light orchestration
  ↓
FastAPI application API
  - chat orchestration
  - retrieval orchestration
  - ingestion/job control
  - memory services
  ↓                    ↘
Job worker / async tasks  LLM provider(s)
  ↓
Postgres (+ pgvector) as system of record
  - sources, chunks, embeddings, memory, chats, jobs, evals
Blob/file storage for raw artifacts when needed
```

For this repo, **Next.js should become the stable public boundary** and **FastAPI should become the private application service**. The browser should not call FastAPI directly. Next Route Handlers are a good fit for a backend-for-frontend layer, but the Next.js docs explicitly position them as an API layer rather than a full backend replacement. That matches this project: keep heavy RAG, ingestion, and memory logic in FastAPI, and use Next for session-aware web-facing endpoints and deployment-safe request brokering. [HIGH confidence]

For storage, the rebuilt system should move toward **Postgres + pgvector** as the long-term default instead of continuing to let Chroma act as the main persisted system boundary. This product needs structured entities (sources, notes, jobs, memory, chat sessions, citations, ingestion state) in addition to vectors. pgvector lets vectors live with relational data and supports exact and approximate search, filtering, and scaling patterns inside Postgres. Chroma is still useful as a transitional adapter, but not as the main long-term boundary for this brownfield rebuild. [MEDIUM-HIGH confidence]

## Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| Next.js app shell | Navigation, layouts, authenticated UX, research workspace views, ingestion UX, chat UX | Browser, BFF handlers |
| Next.js BFF layer | Web-facing `/api/*` endpoints, auth/session checks, input validation, rate limiting, request shaping, SSE/stream relay if used | FastAPI, browser |
| FastAPI API layer | Internal API contract for chat, retrieval, source management, memory, jobs, admin/debug | Next.js BFF, worker |
| Chat application service | Turns user intent into grounded responses, selects retrieval strategy, attaches citations, writes conversation events | Retrieval service, memory service, LLM client, Postgres |
| Retrieval service | Query rewriting, source/topic filtering, vector search, optional reranking, citation packaging | Postgres/pgvector or Chroma adapter, embedding provider |
| Ingestion service | Accepts source submissions, normalizes metadata, creates ingestion jobs, stores raw source records | Worker, Postgres, file/blob storage |
| Worker / job runner | Fetch transcript, parse notes, chunk, summarize, tag, embed, index, run post-ingestion checks | Ingestion service, retrieval store, LLM/embedding providers |
| Memory service | Stores and retrieves user goals, trusted sources, durable preferences, saved insights, conversation-derived memory candidates | Postgres, chat service |
| LLM/embedding gateway | Small wrapper around external/local models with one internal contract, timeouts, retries, observability | Chat, ingestion worker, retrieval |
| Postgres (+ pgvector) | Source of truth for app entities plus vector index | FastAPI services, worker |
| Blob/file storage | Optional storage for transcripts, cleaned markdown, exports, attachments | Ingestion service, worker |
| Evaluation/observability module | Prompt/version tracking, latency, retrieval quality checks, failure logs | Chat, retrieval, ingestion |

## Boundary Rules

1. **Browser talks only to Next.js.**
   - Fixes the current hardcoded-localhost failure mode.
   - Gives one place for auth, quotas, headers, and deployment switching.

2. **Next.js does not own RAG business logic.**
   - Keep Route Handlers thin: validate request, enforce session/rate limits, call FastAPI, shape response.
   - Do not duplicate orchestration in both TypeScript and Python.

3. **FastAPI owns domain workflows.**
   - chat
   - retrieval
   - ingestion/job control
   - memory management
   - admin/eval endpoints

4. **Worker owns long-running and retryable work.**
   - transcript fetch
   - cleaning
   - chunking
   - embeddings
   - summarization/tagging
   - background memory extraction

5. **One persistence model, not ad hoc files.**
   - Repo-committed Chroma state and runtime artifacts should disappear.
   - Data should be reconstructible from raw source records and jobs.

## Recommended Internal Modules

### Next.js

```text
app/
  (workspace)/chat
  (workspace)/sources
  (workspace)/memory
  api/chat/route.ts
  api/sources/route.ts
  api/ingest/route.ts
lib/server/
  auth.ts
  api-client.ts
  rate-limit.ts
  schemas.ts
```

Use Route Handlers for the public web API. Next.js official guidance supports using Route Handlers for backend-for-frontend and proxy patterns, with validation before forwarding requests. [HIGH confidence]

### FastAPI

```text
api/
  main.py
  dependencies.py
  routers/
    chat.py
    ingest.py
    sources.py
    memory.py
    admin.py
  services/
    chat_service.py
    retrieval_service.py
    memory_service.py
    source_service.py
    job_service.py
  providers/
    llm.py
    embeddings.py
    transcript.py
    vector_store.py
  repositories/
    sources.py
    chats.py
    memory.py
    jobs.py
  workers/
    ingest_worker.py
    memory_worker.py
```

FastAPI’s `APIRouter` pattern is the right structure here: keep main app assembly small, group routes by domain, and attach shared dependencies at router boundaries. [HIGH confidence]

## Data Model Shape

Use explicit entities instead of only topic-named vector collections.

### Core entities

- `source`
  - id, type (`youtube`, `note`, `manual`)
  - title, canonical_url, author, imported_at
  - raw_text, cleaned_text, status
  - user tags, trusted flag, topic_id

- `source_chunk`
  - id, source_id, chunk_index
  - text, token_count, metadata_json
  - embedding

- `topic`
  - id, slug, name, description

- `chat_session`
  - id, title, created_at, last_active_at

- `chat_message`
  - id, session_id, role, text, citations_json
  - retrieval_trace_id, model_config_id

- `memory_item`
  - id, kind (`goal`, `preference`, `trusted_source`, `insight`, `follow_up`)
  - text, status (`candidate`, `accepted`, `archived`), source_ref

- `ingestion_job`
  - id, source_id, stage, status, error, started_at, completed_at

- `evaluation_run`
  - id, prompt_version, query, result_summary, score

This supports the product direction better than “topic collection + raw chat response” because memory and ingestion need durable records, not only embeddings.

## Data Flow

### 1. Chat request flow

1. Browser submits a chat request to **Next `/api/chat`**.
2. Next Route Handler validates payload, enforces session/auth/rate limits, and forwards to **FastAPI internal chat endpoint**.
3. FastAPI chat service loads:
   - recent conversation state
   - active topic/workspace context
   - relevant memory items
   - retrieval candidates from the retrieval service
4. Retrieval service performs:
   - query normalization / optional rewrite
   - metadata filtering (`topic`, trusted sources, source type)
   - vector search
   - optional rerank
   - citation packaging
5. Chat service builds grounded prompt with clear source boundaries.
6. LLM gateway calls the model provider with strict timeout/retry policy.
7. Chat service stores message, citations, latency, and retrieval trace.
8. FastAPI returns structured answer payload.
9. Next returns web-safe response to browser.

### 2. Ingestion flow

1. User submits a YouTube URL or pasted notes in the web app.
2. Browser posts to **Next `/api/ingest`**.
3. Next validates and forwards to FastAPI ingestion endpoint.
4. FastAPI creates `source` + `ingestion_job` records immediately and returns job ID.
5. Worker executes stages:
   - fetch transcript / accept pasted text
   - normalize and clean text
   - produce summary/tags
   - chunk
   - embed
   - write vectors and chunk records
   - run ingestion QA checks
6. UI polls job status or receives updates.
7. Completed source becomes searchable and visible in workspace.

### 3. Memory flow

1. During or after a chat, the system identifies candidate memories.
2. Candidate memories are stored separately from durable accepted memory.
3. User can review/accept/edit important memories in a dedicated memory view.
4. Only accepted memory is injected by default into future chats.

This prevents a common failure mode in personal AI tools: silently turning every chat utterance into “memory” and poisoning retrieval.

### 4. Evaluation flow

1. Sample queries or saved chats are replayed against retrieval/chat configs.
2. System logs retrieved chunks, answer, citations, latency, and quality notes.
3. Failures feed prompt/retrieval tuning before adding more “agent” behavior.

## Patterns to Follow

### Pattern 1: Backend-for-Frontend at the web edge
**What:** Use Next Route Handlers as the only public API surface for the browser.
**When:** Immediately, before new feature work.
**Why:** Fixes broken deployment assumptions, centralizes auth/rate limiting, and avoids exposing FastAPI directly.

### Pattern 2: Thin routes, thick services
**What:** Route files only validate and delegate; services hold domain logic.
**When:** For both Next handlers and FastAPI routers.
**Why:** Brownfield code already suffers from large, stateful UI and brittle backend imports.

### Pattern 3: Jobs for ingestion, request-response for chat
**What:** Keep chat synchronous/streaming; move ingestion and enrichment off the request path.
**When:** As soon as ingestion assistant features start.
**Why:** Transcript fetch, chunking, embeddings, and summarization are long-running and failure-prone.

FastAPI supports `BackgroundTasks`, but its docs recommend creating resources for background tasks inside the task itself; for this project, use that only for small follow-up actions and prefer a worker/job model for real ingestion pipelines. [HIGH confidence]

### Pattern 4: Explicit retrieval contracts
**What:** Retrieval service returns structured results: `chunk_id`, `source_id`, `score`, `citation`, `snippet`, `reason`.
**When:** Before tuning prompt quality.
**Why:** You cannot debug groundedness if retrieval returns only loose text blobs.

### Pattern 5: Memory as a separate subsystem
**What:** Separate tables, review flow, and retrieval policy for memory.
**When:** Before “adaptive coach” behavior.
**Why:** Personal memory has different trust and decay rules than source documents.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Browser → FastAPI direct coupling
**Why bad:** Recreates current localhost/deployment breakage and bypasses web-layer controls.
**Instead:** Browser → Next BFF → FastAPI.

### Anti-Pattern 2: One giant chat component
**Why bad:** UI changes, transport changes, and workflow changes collide.
**Instead:** Separate presentation, transport hooks, chat session state, and source/citation panels.

### Anti-Pattern 3: Treating vectors as the primary data model
**Why bad:** Makes jobs, memories, source provenance, and evaluation hard to reason about.
**Instead:** Structured records first, vectors as an index over source and memory text.

### Anti-Pattern 4: Adding broad agent orchestration before evals
**Why bad:** Makes failures harder to localize and hides weak retrieval behind tool loops.
**Instead:** Stabilize ingestion, retrieval, citations, and memory boundaries first.

### Anti-Pattern 5: Request-path double generation by default
**Why bad:** Current code already pays for multiple model passes in the hot path.
**Instead:** Single-pass answer first; optional critique/reflection only in debug/eval modes.

## Brownfield Migration Advice

### Phase 0: Stabilize the seam
- Remove direct browser calls to FastAPI.
- Replace invalid App Router API usage with real `route.ts` handlers.
- Hide debug/raw backend output from public responses.
- Add one internal API client contract between Next and FastAPI.

### Phase 1: Reshape backend around services
- Refactor FastAPI into routers + services + providers.
- Keep current Chroma retrieval behind a `vector_store` adapter so behavior remains intact during migration.
- Add tests around chat response shape, retrieval calls, and router wiring before major storage changes.

### Phase 2: Introduce durable app data
- Add Postgres for sources, chats, jobs, and memory even if vectors remain in Chroma temporarily.
- Start storing ingestion/job state and source metadata outside filesystem conventions.

### Phase 3: Migrate vector storage deliberately
- Add pgvector-backed retrieval adapter.
- Dual-write new ingestions to Postgres/pgvector and existing Chroma during migration if needed.
- Compare retrieval quality and latency before cutting over.

### Phase 4: Add ingestion assistant and memory workflows
- Only after source/job state is durable.
- Build reviewable summaries/tags/memory candidates, not silent automatic mutations.

### Phase 5: Add evaluation and reliability tooling
- Saved test prompts
- retrieval trace inspection
- latency/error dashboards
- regression checks for grounding/citations

This order is safer than “rewrite everything into one new stack” because it preserves the currently working retrieval core while fixing the public boundary first.

## Suggested Build Order / Dependency Implications

1. **Public boundary repair**
   - Build: Next BFF route handlers, shared schemas, internal API client
   - Depends on: nothing
   - Unblocks: deployability, auth, throttling, safe browser flow

2. **Backend modularization**
   - Build: FastAPI routers/services/providers split
   - Depends on: stable internal request contract
   - Unblocks: adding ingestion, memory, tests without more brittle imports

3. **Workspace UX split**
   - Build: dedicated views for chat, sources, source detail, ingestion, memory
   - Depends on: public boundary repair
   - Unblocks: daily-use workflow improvement without backend confusion

4. **Durable relational data layer**
   - Build: Postgres schema for sources, chats, jobs, memory
   - Depends on: backend modularization
   - Unblocks: reliable ingestion tracking, memory, future multi-user path if ever needed

5. **Async ingestion pipeline**
   - Build: job runner, job status, transcript/note normalization pipeline
   - Depends on: durable data layer
   - Unblocks: ingestion assistant features and safer retries

6. **Retrieval upgrade**
   - Build: retrieval abstraction, pgvector adapter, rerank/citation improvements
   - Depends on: durable data layer; preferably async ingestion
   - Unblocks: grounded chat quality and lower operational weirdness

7. **Memory subsystem**
   - Build: candidate memory extraction, review UI, injection policy
   - Depends on: durable data layer, stable chat traces
   - Unblocks: adaptive coaching without polluting source retrieval

8. **Evaluation + observability**
   - Build: prompt/version tracking, retrieval traces, regression suite
   - Depends on: stable chat and retrieval services
   - Unblocks: safe iteration on prompts, memory, and future agent workflows

9. **Narrow agent workflows**
   - Build: source cleanup, tagging suggestions, summary refresh, follow-up generation
   - Depends on: ingestion jobs, evals, memory boundaries
   - Unblocks: future assistant automation without broad autonomy risk

## Scalability Considerations

| Concern | At 100 users | At 10K users | At 1M users |
|---------|--------------|--------------|-------------|
| App traffic | One Next deployment + one FastAPI instance is enough | Separate public web and private API scaling | Queueing, regionalization, stronger auth/limits |
| Retrieval | Exact or light approximate search is fine | pgvector indexes + metadata filters + reranking | Partitioning/replicas/sharding as needed |
| Ingestion | Single worker is fine | Dedicated workers and retry policies | Distributed workers and provider backpressure controls |
| Memory | Simple reviewed memory table | Memory policies by type and recency | Needs stronger ranking and lifecycle management |
| Evaluation | Manual saved cases | Scheduled regression runs | Formal eval pipeline and offline benchmarking |

For this product’s stated v1 constraints, design for **clean single-user reliability first**, not for premature large-scale multi-tenancy.

## Opinionated Recommendation

The best architecture for this rebuild is:

- **Next.js as the only browser-facing boundary**
- **FastAPI as the domain/backend engine**
- **job worker for ingestion and enrichment**
- **Postgres + pgvector as the long-term source of truth**
- **retrieval and memory as separate services with explicit contracts**

Do **not** collapse everything into Next.js, and do **not** keep the current “browser → FastAPI → local vector store/filesystem” shape as the long-term design. It is too fragile for reliable daily use, memory, and future agent workflows.

## Sources

- Next.js docs: Backend-for-Frontend guide, Route Handlers, proxy pattern, security caveats, 2026-04-15 — https://nextjs.org/docs/app/guides/backend-for-frontend [HIGH]
- FastAPI docs: Bigger Applications / APIRouter — https://fastapi.tiangolo.com/tutorial/bigger-applications/ [HIGH]
- FastAPI docs: Background Tasks / dependency guidance — verified via Context7 on `/fastapi/fastapi` [HIGH]
- Chroma docs: Manage Collections — https://docs.trychroma.com/docs/collections/manage-collections [MEDIUM]
- pgvector official README/docs — https://github.com/pgvector/pgvector [HIGH]
- Brownfield repo context — `.planning/PROJECT.md`, `.planning/codebase/STACK.md`, `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/CONCERNS.md` [HIGH]
