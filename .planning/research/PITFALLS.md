# Domain Pitfalls

**Domain:** Brownfield personal AI research workspace and coaching assistant rebuilt from a transcript-based RAG app
**Researched:** 2026-04-22

## Critical Pitfalls

Mistakes that usually force rewrites, destroy trust, or make the product feel worse as it gets more personalized.

### Pitfall 1: Retrieval truthiness without proof
**What goes wrong:** The assistant sounds grounded because it answers confidently from a vector search, but it cannot reliably show which transcript chunk or note justified the answer.
**Why it happens:** Teams treat “RAG works” as “similar chunks were returned once,” skip citation UX, and do not evaluate whether the retrieved evidence actually supports the answer.
**Consequences:** Users stop trusting answers, coaching advice becomes hard to validate, and memory features amplify wrong conclusions instead of helping.
**Warning signs:**
- Answers reference vague “your sources” instead of specific notes/videos
- Retrieved chunks are semantically related but not actually sufficient to answer the question
- Prompt changes seem to help quality more than retrieval improvements
- Users re-open the original transcript because the product cannot show enough evidence inline
**Prevention:**
- Make source attribution a product requirement, not a future enhancement
- Store stable source IDs, timestamps, titles, topic tags, and chunk provenance at ingest time
- Add retrieval and answer-grounding evaluations before adding coaching depth
- Show the exact supporting excerpts in the UI, not just document names
- Separate “answerable from current sources” from “speculative coaching suggestion” in response formatting
**Detection:** Sudden jumps in “sounds good but I can’t verify it” feedback, or frequent disagreement between cited chunks and generated answers.
**Phase to address:** Phase 1 - Grounding and retrieval hardening

### Pitfall 2: Treating raw transcripts as clean knowledge
**What goes wrong:** Low-signal transcripts, bad punctuation, ads, sponsor segments, and speaker drift are ingested as if they were trustworthy knowledge objects.
**Why it happens:** Rebuilds often preserve the old ingestion path and optimize for “URL in, chat out” instead of source quality.
**Consequences:** Retrieval becomes noisy, summaries inherit junk, topic collections fill with near-duplicates, and the assistant learns the wrong emphasis from noisy content.
**Warning signs:**
- Retrieved chunks contain intro banter, CTA language, or transcript artifacts
- The same source gets re-ingested with slightly different cleaned text
- Users need to manually explain what part of a video mattered after ingesting it
- “Useful source” and “stored source” diverge sharply
**Prevention:**
- Put the first narrow agent workflows in ingestion, exactly as the product direction intends
- Require a cleaning pass that strips boilerplate and preserves timestamps/provenance
- Add source-level metadata: author, trust level, topic, summary, key claims, and why this source matters
- Support human review/edit before content becomes retrievable for chat
- Keep raw transcript, cleaned text, and derived summaries as separate layers
**Detection:** Increasing retrieval length with declining usefulness; ingest success metrics look good while answer quality does not.
**Phase to address:** Phase 2 - Ingestion workflow rebuild

### Pitfall 3: Mixing durable memory with transient chat context
**What goes wrong:** Goals, preferences, chat history, transcript facts, and temporary task context all get blended into one retrieval surface.
**Why it happens:** Personal AI products try to “remember everything” before defining memory classes and promotion rules.
**Consequences:** Coaching becomes intrusive or inconsistent, stale assumptions resurface, and one bad inference can keep contaminating future answers.
**Warning signs:**
- The system cannot explain whether a claim came from a source, a past chat, or an inferred preference
- Old chats dominate results for unrelated queries
- “Memory” grows quickly but usefulness does not
- Users feel the assistant is overconfident about goals or habits they never explicitly confirmed
**Prevention:**
- Split storage into at least: source knowledge, explicit personal memory, and ephemeral session context
- Only promote memory through explicit save/confirm flows or narrow heuristics with review
- Version and timestamp memory items; allow easy edit, demote, archive, and delete
- Keep coaching prompts aware of memory confidence and recency
- Never let inferred memory outrank explicit user-authored notes by default
**Detection:** Memory-related corrections become common, or the same false assumption keeps reappearing across chats.
**Phase to address:** Phase 4 - Personal memory and coaching

### Pitfall 4: Rebuilding UI while preserving broken boundaries
**What goes wrong:** The app looks newer, but the old frontend/backend contract, routing drift, and duplicated flows remain underneath.
**Why it happens:** Brownfield teams patch visible UX first and postpone boundary cleanup because the legacy path “mostly works.”
**Consequences:** Every new feature has to work around brittle seams; deployment, auth, and testing stay painful; small changes break unrelated paths.
**Tie to this repo:** Current concerns already show hardcoded localhost networking, an invalid App Router API file, brittle backend imports, and duplicate chat UI components.
**Warning signs:**
- Browser code still calls FastAPI directly with environment-specific URLs
- There are multiple chat transport paths or duplicate components implementing the same flow
- Backend router/setup issues are treated as local quirks instead of architecture defects
- New features require touching routing, transport, and UI in one change
**Prevention:**
- Define one supported web boundary early: either a real Next server bridge or a consciously separate backend API contract
- Delete or archive duplicate UI paths before adding new workspace features
- Normalize config/env handling into one authoritative contract
- Make boundary cleanup a prerequisite for feature expansion, not a cleanup phase
**Detection:** Repeated “works locally, breaks in deploy” incidents and PRs that modify many unrelated layers for one user-visible change.
**Phase to address:** Phase 0/1 - Foundation and boundary hardening

### Pitfall 5: Leaving debug and admin visibility on the public path
**What goes wrong:** Debug payloads, retrieved context, raw model outputs, and test endpoints remain available because they helped during prototyping.
**Why it happens:** Personal-first products often underweight security because there is only one intended user.
**Consequences:** Privacy leaks, prompt leakage, unnecessary token cost, and an API surface that is risky to expose beyond localhost.
**Tie to this repo:** `CONCERNS.md` already flags raw model output on `POST /chat`, exposed retrieval/debug behavior on `/test_llm`, and no auth or throttling on expensive endpoints.
**Warning signs:**
- API responses include raw completions or hidden reasoning/debug fields
- Diagnostic endpoints sit on the same router as user-facing chat
- Expensive inference routes are callable without auth, quotas, or rate limits
- Logs include source text or personal notes verbatim
**Prevention:**
- Split public, admin, and debug routes immediately
- Remove raw/debug fields from user responses by default
- Add authentication, rate limiting, and request logging before any hosted exposure
- Redact logged content and avoid storing raw personal text unless necessary
**Detection:** Security review finds sensitive payloads in logs or network traces; cost spikes with no corresponding user growth.
**Phase to address:** Phase 1 - Production-safe API boundary

### Pitfall 6: No evaluation harness for retrieval, ingest, and regressions
**What goes wrong:** The team judges quality by ad hoc prompting instead of repeatable tests and eval datasets.
**Why it happens:** RAG products can feel demo-ready long before they are stable, so engineering discipline lags behind perceived progress.
**Consequences:** Chunking changes, prompt tweaks, or ingestion cleanup silently break answer quality; reliability never compounds.
**Tie to this repo:** The codebase has no automated regression suite, no frontend tests, and no framework-managed ingestion tests; current “tests” are manual scripts over live data.
**Warning signs:**
- “It seemed better yesterday” is the main quality signal
- Production data doubles as the only test fixture
- Retrieval bugs are found by users, not CI
- Engineers fear refactoring chat or ingestion code because there is no safety net
**Prevention:**
- Create a small gold set of user questions with expected supporting sources and acceptable answers
- Add API contract tests for chat payload shape and source attribution
- Add ingestion tests for cleaning, dedupe, metadata extraction, and collection writes
- Keep fast offline fixtures instead of relying on committed runtime vector data
- Track eval results across prompt, chunking, and retrieval changes
**Detection:** Frequent subjective quality debates with no artifact to compare runs.
**Phase to address:** Phase 1 - Reliability harness

### Pitfall 7: Building a “coach” before earning trust as a workspace
**What goes wrong:** The product starts making motivational or behavioral suggestions before retrieval, note organization, and source trust are solid.
**Why it happens:** Coaching feels like the differentiator, so teams rush into persona and memory features before basic workspace utility is dependable.
**Consequences:** Advice feels generic, occasionally fabricated, or emotionally miscalibrated; users disengage because the assistant has not yet earned authority.
**Warning signs:**
- The assistant gives prescriptive advice when it lacks grounded evidence
- Users mainly use the app to verify what it said rather than to accelerate their work
- Retrieval reliability issues are reframed as prompt/persona issues
- Coaching outputs are longer and more polished than the evidence behind them
**Prevention:**
- Sequence roadmap around trustworthy workspace actions first: ingest, clean, organize, retrieve, cite
- Restrict early coaching to source-backed reflections and follow-up questions
- Require explicit indication when guidance is based on user memory vs curated sources vs general reasoning
- Add “I don’t have enough grounded context” as a success case, not a failure case
**Detection:** Users trust summaries and snippets less after coaching features launch.
**Phase to address:** Phase 3 before Phase 4 - Workspace reliability before adaptive coaching

### Pitfall 8: Cost and latency creep from invisible hot-path work
**What goes wrong:** Each user message triggers unnecessary retrieval scans, second-pass reflection calls, oversized prompts, or duplicate model requests.
**Why it happens:** Prototype logic stays in the request path because it improved quality once and no one added observability or budgets.
**Consequences:** The app feels slow, costs rise, and “cheap personal tool” goals get undermined by architecture drift.
**Tie to this repo:** Current chat flow can spend two 120-second model timeouts, and retrieval performs full-collection metadata scans on every query.
**Warning signs:**
- P95 latency is high even for simple questions
- Token usage and runtime cost are not measured per route
- Debug inspection work runs on every request
- Quality improvements depend on adding more prompt/context rather than pruning bad work
**Prevention:**
- Set latency and per-query cost budgets now
- Remove debug scans from hot paths and make second-pass generation optional
- Instrument retrieval time, model time, token counts, and fallback rates
- Keep context windows intentionally small and source-ranked
- Prefer cheap deterministic preprocessing in ingestion over expensive runtime cleanup
**Detection:** Users ask fewer follow-ups because each turn feels too slow, or infra costs grow faster than usage.
**Phase to address:** Phase 1 - Performance and observability hardening

## Moderate Pitfalls

### Pitfall 1: Topic taxonomy drift
**What goes wrong:** Topics/collections are created ad hoc, overlap semantically, and stop matching how the user actually thinks.
**Warning signs:** Similar queries must be tried across multiple topics; sources fit in several places; old collections are never reused confidently.
**Prevention:** Start with a small controlled taxonomy, allow aliases, and support source reclassification without re-ingesting everything.
**Phase to address:** Phase 2 - Ingestion and organization

### Pitfall 2: Provenance loss during summarization
**What goes wrong:** Summaries become the main retrieved artifact, but the app can no longer connect them back to exact transcript spans or note passages.
**Warning signs:** Great summaries, weak citations; derived notes outrank originals; timestamp/source links disappear after processing.
**Prevention:** Keep derived artifacts linked to original chunk IDs and preserve timestamp/source references in every layer.
**Phase to address:** Phase 2 - Ingestion and derived artifacts

### Pitfall 3: Environment and dependency drift in a brownfield stack
**What goes wrong:** Local setup depends on which requirements file, model URL, or route path happened to be used last.
**Tie to this repo:** Python dependencies are split, backend docs and config disagree, and runtime artifacts are committed.
**Warning signs:** Fresh setup instructions fail; one machine can ingest while another cannot; committed vector data masks broken setup.
**Prevention:** Collapse to one dependency manifest per runtime, remove generated artifacts from git, and verify a clean bootstrap path in CI.
**Phase to address:** Phase 0 - Repo sanitation

## Minor Pitfalls

### Pitfall 1: Letting archived code stay plausible
**What goes wrong:** Old or duplicate files remain close enough to active code that future work accidentally revives them.
**Tie to this repo:** `Proxy.tsx` duplicates chat behavior and already contains hard failures.
**Warning signs:** Engineers reference the wrong file; dead code still imports real endpoints; behavior differs between near-identical components.
**Prevention:** Delete dead paths or move them to a clearly non-runtime archive location.
**Phase to address:** Phase 0 - Cleanup

### Pitfall 2: Operational scripts drift away from live data model
**What goes wrong:** Maintenance scripts keep old assumptions about collection names, config exports, or schema shape.
**Tie to this repo:** Existing Chroma inspection scripts already mismatch the current topic-per-collection model.
**Warning signs:** “Debug” scripts fail unless edited manually; no one trusts maintenance tooling.
**Prevention:** Either test and maintain these scripts as real tools or delete them and replace with one supported admin path.
**Phase to address:** Phase 1 - Admin/debug tooling hardening

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Foundation cleanup | Shipping new UI on top of broken boundaries | Fix transport, routing, env contract, duplicate components, and repo artifacts before feature work |
| Retrieval hardening | Mistaking fluent answers for grounded answers | Add citation UX, source provenance, and retrieval evals before deeper assistant behavior |
| Ingestion assistant | Automating dirty transcript ingestion faster | Put agent help into cleaning, tagging, dedupe, and review, not just summarization |
| Personal memory | Storing inferred preferences as durable truth | Separate memory classes, require confirmation, and support edit/delete/versioning |
| Coaching | Giving advice unsupported by retrieved evidence | Gate coaching to grounded reflections until workspace trust is high |
| Deployment | Exposing debug surfaces and costly endpoints | Separate admin/public routes, add auth, rate limits, and observability |
| Testing | Using live Chroma data as the only quality signal | Build small offline fixtures and regression/eval suites tied to real user questions |

## Sources

- Internal product brief: `/Users/jayden77/dev/better-everyday-v3/.planning/PROJECT.md`
- Internal codebase concerns: `/Users/jayden77/dev/better-everyday-v3/.planning/codebase/CONCERNS.md`
- Internal testing analysis: `/Users/jayden77/dev/better-everyday-v3/.planning/codebase/TESTING.md`
