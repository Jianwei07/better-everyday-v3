# Project Research Summary

**Project:** Better Everyday
**Domain:** Personal AI research workspace and adaptive coaching assistant
**Researched:** 2026-04-22
**Confidence:** HIGH

## Executive Summary

Better Everyday should be rebuilt as a personal-first AI research workspace, not as a generic chatbot or broad agent platform. The research consistently points to a product centered on trusted personal sources—starting with YouTube transcripts and user notes—organized into bounded workspaces, queried through grounded chat, and surfaced with evidence the user can inspect. Experts build products in this category by investing first in ingestion quality, source organization, retrieval quality, and citation UX; personalization and coaching come only after the workspace earns trust.

The strongest implementation direction is a low-ops web app on Next.js with a stable browser-facing boundary, durable Postgres-backed storage, hybrid retrieval, and a narrow asynchronous ingestion pipeline. Across the research, the clearest product recommendation is: make v1 excellent at ingesting, cleaning, organizing, retrieving, and saving insights from curated sources. The first differentiated AI feature should be a human-in-the-loop ingestion assistant, not a full coach.

The main risks are also consistent across files: weak provenance, dirty transcript ingestion, blurred memory boundaries, and preserving the repo's broken browser/backend seams during the rebuild. Those risks are mitigated by making citations and provenance a hard requirement, separating source knowledge from durable memory, moving long-running ingest work off the request path, and repairing the web/API boundary before expanding feature scope.

## Key Findings

### Recommended Stack

The stack research recommends a pragmatic, low-cost rebuild: Next.js-first TypeScript on Vercel for the public product surface, Supabase Postgres with pgvector as the single source of truth, and a small Python worker limited to ingestion and offline ML utilities. The key theme is simplification: remove the brittle browser-to-FastAPI split from the public UX path, unify state in Postgres, and keep Python only where it materially helps.

**Core technologies:**
- **Next.js 16 + React 19 + TypeScript 5**: web app, public API boundary, and main product runtime — best fit for a web-only personal AI product with streaming and server/client separation.
- **Vercel AI SDK 6**: chat streaming, model abstraction, and narrow tool use — keeps generation provider-swappable without heavyweight orchestration.
- **Supabase Postgres + pgvector**: primary database plus vector retrieval — unifies chats, sources, jobs, memory, and retrieval state in one durable system.
- **Postgres full-text search + pgvector hybrid retrieval**: lexical + semantic retrieval — better grounding than vector-only search for transcripts and notes.
- **Drizzle ORM**: schema and migrations — lightweight relational tooling while leaving retrieval-heavy queries explicit.
- **Python 3.12+ worker**: transcript fetch, cleaning, chunking, embeddings, repair scripts — useful off the request path, but not as the app's public backbone.

Critical version direction: Next.js 16.x, React 19.x, TypeScript 5.x, Vercel AI SDK 6.x, pgvector 0.8.x, Python 3.12+.

### Expected Features

The research is clear that v1 must feel like a trustworthy research desk, not a transcript demo. Table stakes are reliable ingestion, bounded workspaces, grounded chat with inspectable evidence, search/browse, and note capture. Differentiation should come from better source handling and later from explicit, controllable personalization.

**Must have (table stakes):**
- YouTube URL import and pasted note/transcript ingestion.
- Source normalization with editable summaries and tags.
- Workspace/topic organization with source-scoped retrieval controls.
- Grounded chat with inline citations or quote-level evidence.
- Search and browse across sources, notes, and summaries.
- Save useful outputs as notes with citation retention.
- Clear failure behavior when evidence is insufficient.
- Basic workspace-scoped chat history.

**Should have (competitive):**
- Workspace-first UI with dedicated source, notes, and chat panes.
- Human-in-the-loop ingestion assistant for cleanup, tagging, summarization, and organization.
- Trusted-source controls and later evidence-first answer views.

**Defer (v2+):**
- Goal-aware coaching and prior-chat memory retrieval.
- Daily resurfacing/review loops.
- Broad web research and autonomous agents.
- Multi-user/family support.
- Audio/video/visual artifact generation.

### Architecture Approach

The architecture research recommends a four-layer system: browser → Next.js BFF/public web boundary → FastAPI domain services → async worker, all backed by Postgres + pgvector. The key architectural guidance is to repair boundaries first. The browser should talk only to Next.js; Next should stay thin and own auth, validation, and request brokering; FastAPI should own domain workflows such as chat, retrieval, ingestion, and memory; and long-running ingest/enrichment work should run as jobs, not on the hot path.

**Major components:**
1. **Next.js app + BFF** — authenticated workspace UI and the only browser-facing API surface.
2. **FastAPI domain layer** — chat, retrieval, source management, memory, and internal admin/eval workflows.
3. **Worker / job runner** — transcript fetch, cleaning, chunking, summaries, embeddings, and retryable ingest tasks.
4. **Postgres + pgvector** — system of record for sources, chunks, chats, jobs, memory, citations, and evaluation traces.

### Critical Pitfalls

The biggest risks are not flashy technical failures; they are trust failures. The research repeatedly warns that a personal AI product becomes unusable when it sounds smart but cannot prove what it knows, or when personalization quietly accumulates wrong assumptions.

1. **Retrieval truthiness without proof** — require stable provenance, exact supporting excerpts, and answer-grounding evals before deeper coaching features.
2. **Treating raw transcripts as clean knowledge** — keep raw, cleaned, and derived layers separate; add cleaning, metadata, dedupe, and review in the ingest flow.
3. **Mixing durable memory with transient chat context** — separate source knowledge, accepted memory, and ephemeral session context with explicit review/edit flows.
4. **Rebuilding UI while preserving broken boundaries** — fix browser/API seams, duplicate flows, and env contracts before adding feature breadth.
5. **No evaluation harness** — add retrieval, ingest, and API contract tests early so quality can compound instead of regressing silently.

## Implications for Roadmap

Based on the combined research, the roadmap should prioritize trust foundations before personalization. The right phase structure is one that first fixes the product boundary and data model, then makes ingestion and retrieval reliable, then adds workflow intelligence, and only then introduces memory-driven coaching.

### Phase 1: Foundation and Boundary Repair
**Rationale:** The current repo's biggest blocker is broken seams, not missing AI features. Everything else compounds on a stable public boundary.
**Delivers:** Next.js route handlers/BFF, shared schemas, internal API contract, cleaned env/config handling, removal of duplicate/dead public paths, production-safe auth/rate-limit/debug separation.
**Addresses:** Workspace-first rebuild, deploy-safe web flow, clear answer surfaces.
**Avoids:** Preserving broken boundaries, exposing debug/admin paths, local-only networking drift.

### Phase 2: Durable Workspace Core
**Rationale:** Before improving answers, the app needs durable records for sources, chats, jobs, notes, and workspace structure.
**Delivers:** Postgres schema, topic/workspace model, source metadata, note model, chat/session persistence, basic search/browse foundations.
**Uses:** Supabase Postgres, Drizzle, relational + JSONB modeling.
**Implements:** Explicit domain entities instead of vector-collection-only state.

### Phase 3: Ingestion and Grounded Retrieval
**Rationale:** v1 value lives or dies on clean ingest and trustworthy evidence-backed answers.
**Delivers:** YouTube/note ingestion, normalization pipeline, async jobs, chunking, embeddings, hybrid retrieval, citations, source controls, failure behavior, searchable sources.
**Addresses:** Core v1 table stakes.
**Avoids:** Dirty transcript ingestion, retrieval truthiness, provenance loss, hot-path latency creep.

### Phase 4: Daily-Use Workspace UX
**Rationale:** Once the data and retrieval layers are trustworthy, the product should feel like a real workspace instead of a thin chat shell.
**Delivers:** Source pane, notes pane, chat pane, source detail views, save-to-notes workflows, better workspace re-entry, evidence-first answer presentation.
**Addresses:** Search/browse, notes reuse, workspace-first UI, inspectable trust signals.
**Avoids:** Overinvesting in coaching before the workspace is genuinely useful.

### Phase 5: Ingestion Intelligence
**Rationale:** The safest first differentiated AI behavior is reviewable help during ingest.
**Delivers:** Human-in-the-loop cleanup suggestions, tags, summaries, topic placement, source organization recommendations.
**Addresses:** Best early differentiator from FEATURES.md.
**Avoids:** Broad autonomous agents and opaque auto-mutations.

### Phase 6: Memory and Adaptive Coaching
**Rationale:** Personal memory should only arrive after source trust, retrieval quality, and evaluation are stable.
**Delivers:** Explicit goals, trusted-source controls, memory review/accept flows, relevant prior-chat recall, source-grounded coaching prompts and check-ins.
**Addresses:** Long-term product differentiation.
**Avoids:** Memory contamination, intrusive personalization, unsupported advice.

### Phase Ordering Rationale

- Boundary repair comes first because architecture and pitfalls research both identify it as the main brownfield multiplier.
- Durable data precedes advanced retrieval, memory, and jobs because the product needs reconstructible records, not only vectors.
- Ingestion and grounding precede coaching because the product promise is trustworthy recall from curated sources.
- Workspace UX should mature before memory-heavy coaching so users gain daily utility even if personalization remains minimal.
- Narrow agent workflows are safer after jobs, provenance, and evaluation exist.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3:** Retrieval tuning details, chunking strategy, reranking, and YouTube ingestion fallbacks should be validated against the real corpus.
- **Phase 5:** Ingestion assistant review UX and automation thresholds need product-specific experimentation.
- **Phase 6:** Memory ranking, promotion rules, and coaching policy need deeper design/research before implementation.

Phases with standard patterns (skip research-phase):
- **Phase 1:** Next.js BFF, route handlers, auth/rate limiting, and boundary cleanup are well-documented.
- **Phase 2:** Postgres schema, Drizzle migrations, and explicit entity modeling follow standard patterns.
- **Phase 4:** Workspace UI decomposition is mostly product design/execution, not unknown technical research.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Strong agreement across stack and constraints research; based mostly on official docs and direct fit to repo failure modes. |
| Features | MEDIUM-HIGH | Strong product pattern alignment from comparable tools, but some differentiators still need validation against actual daily use. |
| Architecture | HIGH | Clear, opinionated recommendation backed by official framework guidance and brownfield repo realities. |
| Pitfalls | HIGH | Risks are concrete, repo-specific, and strongly aligned with known RAG/product failure modes. |

**Overall confidence:** HIGH

### Gaps to Address

- **FastAPI scope vs TypeScript consolidation:** STACK.md prefers removing Python from the public path entirely, while ARCHITECTURE.md keeps FastAPI as the internal domain layer. Resolve this during planning by choosing one stable ownership model for domain logic.
- **Embedding and reranker choices:** Model specifics are still medium/low-confidence and should be benchmarked on the real transcript/note corpus.
- **Retrieval policy thresholds:** Failure behavior, hybrid search weighting, and citation thresholds need empirical tuning rather than assumption.
- **Memory promotion rules:** The right review/accept flow for goals, trusted sources, and prior-chat relevance remains a design gap until later phases.

## Sources

### Primary (HIGH confidence)
- Next.js docs — Route Handlers and Backend-for-Frontend guidance.
- Vercel AI SDK docs — streaming, tooling, and RAG integration patterns.
- Supabase docs and pgvector README — Postgres-native vector storage and retrieval patterns.
- FastAPI docs — application structure, routers, and background-task guidance.
- Internal project context: `.planning/PROJECT.md`, `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/CONCERNS.md`, `.planning/codebase/TESTING.md`.

### Secondary (MEDIUM confidence)
- NotebookLM, Claude Projects, Readwise Reader, Reflect, and Notion AI product/help docs — feature expectations and workspace patterns.
- YouTube Transcript API and yt-dlp docs — ingestion implementation options.

### Tertiary (LOW confidence)
- Specific local reranker recommendation and exact embedding model choice — useful starting points, but should be validated during implementation.

---
*Research completed: 2026-04-22*
*Ready for roadmap: yes*
