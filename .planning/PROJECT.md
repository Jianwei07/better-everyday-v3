# Better Everyday

## What This Is

Better Everyday is a personal web app that turns YouTube/podcast transcripts and personal notes into a grounded AI research workspace for daily use.

## Core Value

Grounded recall from personally curated sources, so answers are useful, trustworthy, and tied to evidence the user chose.

## Current Direction

- Revive the stale app by pivoting away from the legacy Eva chatbot.
- Keep v1 web-only and personal-first.
- Start with a workspace shell before backend/RAG work.
- Make sources, ingestion, notes, and chat first-class surfaces.
- Keep infrastructure cheap and low-ops.

## Current Phase

Phase 1: Workspace Shell Pivot.

## Constraints

- Do not copy the external skills harness into this repo.
- Do not add family accounts, auth, mobile, billing, or broad agents in v1 slice.
- Do not preserve browser-to-localhost FastAPI as the long-term public flow.
- Do not add backend complexity before the product shell is clear.

## Product Principles

- Source knowledge, durable memory, and transient chat context are separate concerns.
- Reviewable ingestion before automation.
- Evidence-backed answers before coaching.
- Delete/sideline legacy paths instead of keeping parallel confusing flows.
