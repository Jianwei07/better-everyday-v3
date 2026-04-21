# Better Everyday

## What This Is

Better Everyday is a personal web app for turning YouTube transcripts and my own notes into a grounded AI research workspace that I can use daily. It rebuilds the legacy chatbot in this repo into a cleaner, more reliable experience that starts with curated-source chat and grows toward an adaptive coach informed by my goals, trusted sources, and prior conversations.

## Core Value

Grounded recall from personally curated sources so the assistant gives trustworthy answers I will actually use every day.

## Requirements

### Validated

- ✓ User can chat with a web-based assistant against ingested source material — existing
- ✓ User can ingest source content into a topic-scoped Chroma knowledge base — existing
- ✓ User can retrieve topic-specific context and generate answers through an HTTP-served LLM backend — existing
- ✓ User can run the current system as a split Next.js frontend and FastAPI backend — existing

### Active

- [ ] Rebuild the legacy app into a cleaner web app with better UI and flow for daily use
- [ ] Support both YouTube URL import and transcript or note paste as first-class ingestion paths
- [ ] Add ingestion-assistant workflows that help clean, tag, summarize, and organize newly added sources
- [ ] Add personal memory for goals, trusted sources, and relevant prior chats to support adaptive coaching
- [ ] Improve retrieval grounding and answer quality enough that the assistant feels reliable for daily use

### Out of Scope

- Family accounts or shared multi-user experiences — v1 is personal-first to keep memory, privacy, and scope simpler
- Native mobile apps — web app only for v1
- Broad autonomous agent systems — start with narrow ingestion assistance and grounded chat before wider agent orchestration
- Heavy paid infrastructure or resource-hungry model hosting — the project should stay efficient and mostly free to run

## Context

This repository is a brownfield Next.js plus FastAPI plus Chroma RAG project with an existing chat flow, ingestion script, and local retrieval pipeline. The current system already supports topic-based ingestion and chat, but the codebase map shows legacy issues that make it a poor daily-use product today: frontend networking is hardcoded to localhost, the checked-in Next API bridge is not valid for the App Router, backend imports are brittle, public debug output is exposed, and there is no automated regression coverage.

The new direction is to treat the current codebase as a starting point, not a final shape. The product should feel like a personal research workspace first: I ingest YouTube videos and my own notes, organize them into a trustworthy knowledge base, and chat with an assistant that can recall the right context. Over time it should become more personalized by remembering my goals, preferred sources, and useful follow-up context from prior chats.

The initial user is me, though the product may later expand to family members. v1 should therefore optimize for personal utility, privacy, and speed of iteration instead of multi-user complexity. The desired experience is not a generic transcript Q&A bot; it should feel like a grounded assistant with better UI flow and helpful ingestion workflows.

## Constraints

- **Platform**: Web app only for v1 — keep the initial surface area focused and easy to iterate on
- **Compute**: MacBook Pro M5 with 24 GB RAM — avoid designs that require sustained heavy local compute or always-on large models
- **Cost**: Prefer free or near-free infrastructure — use services like Vercel and free-tier data stores where practical
- **Efficiency**: Favor smaller efficient models and strong retrieval over bigger local models — reduce heat, latency, and resource overhead
- **Architecture**: Brownfield rebuild — leverage the existing Next.js, FastAPI, and retrieval code where useful, but fix broken flow and legacy seams
- **Personalization**: Memory should focus on my goals, trusted sources, and prior relevant chats — avoid multi-user account complexity in v1

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Rebuild the legacy experience instead of lightly patching it | The current app already proves the core idea, but the UI, routing, and reliability issues make it a weak base for daily use | — Pending |
| Web app only for v1 | Keeps scope tighter and matches the current codebase strengths | — Pending |
| Personal-first v1 with no family accounts | Personalized memory and coaching are easier to shape for one user before introducing shared or per-user complexity | — Pending |
| Start agent behavior in ingestion workflows | Cleaning, tagging, summarizing, and organizing incoming sources is the clearest first use of agent-style help | — Pending |
| Trust comes from grounded recall before broader coaching features | If retrieval quality is weak, better memory or UI will not make the product useful daily | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-22 after initialization*
