# Eva Health Chatbot: Podcast-Powered RAG for Smarter Health Q&A

![Docker Compose](https://img.shields.io/badge/docker-compose-blue)
![LLM-Ready](https://img.shields.io/badge/LLM-ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Open Source](https://img.shields.io/badge/open--source-yes-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Made with LangChain](https://img.shields.io/badge/langchain-v0.2+-orange)

> **A personal AI project exploring Retrieval-Augmented Generation (RAG) optimization, health data ingestion, and local LLM deployment—turning podcast transcripts into actionable health advice.**

---

## 🚀 Project Purpose

Eva Health Chatbot is a personal, retrieval-augmented assistant that curates and retrieves health and wellness insights from podcast transcripts and curated media. The focus: providing on-demand, category-specific health advice (Neurology, Optometry, Cardiovascular, Fitness, Self-Help, and General Tips).  
This is a sandbox for **experimenting with RAG optimization, ingestion, and LLM infrastructure—creating a tool that helps reinforce learning from real-world listening.**

---

## 🛠️ Frameworks & Techniques Explored

- **RAG Optimization**

  - **Ingestion Pipelines:** Parsing and chunking podcast transcripts, tuning chunk size and overlap.
  - **Retrieval Tuning:** Category/topic-based retrieval, top-k and reranking experimentation.
  - **Rerankers:** Testing cross-encoder rerankers to boost answer relevance.
  - **Expanding Knowledge:** Modular ingestion for easy addition of new health domains.

- **Response Improvements**

  - **Prompt Template Iteration:** Designing prompts for clarity and accuracy.
  - **Self-Attention Loops:** Prototype answer self-checks and re-asking for improved reliability.
  - **Prompt-based Output Optimization:** Dynamically re-evaluating answers for actionable, concise advice.

- **Local & Hybrid Computing**

  - **Local LLM Serving:** Running all services locally in Docker Compose for rapid iteration and zero cloud costs.
  - **Framework Experimentation:** Comparing oLlama, llama.cpp, and Hugging Face APIs for inference and serving.
  - **Resource Optimization:** Balancing performance and compute for UAT/prod and personal use.

- **Testing Next-Gen RAG**
  - **CAG (Contrastive Augmented Generation):** Early experiments with contrastive retrieval/answering.
  - **Multi-Model RAG:** Exploring orchestration of multiple LLMs for robustness.

---

## 🧩 Architecture

- **Backend:** FastAPI (Python) orchestrating all steps with LangChain.
- **LLM Server:** llama.cpp (Phi-2, Q4 GGUF) or oLlama (easy model swaps).
- **Vector Store:** ChromaDB (local, persistent, with category metadata).
- **Frontend:** Next.js (optional, monorepo setup for live chat/dashboard).
- **DevOps:** Docker Compose for all components and volume-mapped storage.

---

## ⚡ Features

- **Podcast-Informed Health Q&A:** Ingests and retrieves advice from podcast transcripts and curated wellness content.
- **Category-Based Retrieval:** Specialized advice for Neurology, Optometry, Cardiovascular, Fitness, Self-Help, and more.
- **Plug-and-Play Ingestion:** Easily expand knowledge with new transcripts, no retraining required.
- **Optimized for Local Computing:** Works entirely offline; no cloud dependency for UAT/prod/dev.
- **RAG Experimentation:** Easy to swap in new retrieval, reranking, or LLM serving approaches.

---

## 🚦 How to Run

```sh
# Build and start everything (from project root)
cat requirements_version.txt | sed 's/[=<>!].*//' | grep -v '^#' | grep -v '^\s*$' | sort -u > requirements.txt
docker-compose up --build

# Or, for code changes only (with volume-mount):
docker-compose build fastapi-backend
docker-compose restart fastapi-backend

# To run backend llm services:
docker-compose up
docker-compose logs -f

```

## 📚 Ingesting Podcast Data

- **Prepare Transcripts:** Convert podcast audio to text (manual or automated), tag by category/topic.
- **Ingestion Script:** Run the Python pipeline to chunk, embed, and store documents in ChromaDB.
- **Ready for RAG:** Eva can now answer questions using the enriched knowledge base.
- python api/add_data.py --data_path <FOLDER_PATH> --category <CATEGORY> --chunk_size <CHUNK_SIZE INT> --chunk_overlap <CHUNK INT>
- example: python api/add_data.py --data_path data/neuro --category neuro --chunk_size 300 --chunk_overlap 100

---

## 🧪 What I’m Experimenting With

- Best chunking and retrieval parameters for accurate health Q&A.
- Pipeline reranking and answer grading with local models.
- Comparing LLM serving solutions (llama.cpp vs oLlama vs HuggingFace TGI).
- Stepback prompting, CAG, and new RAG orchestration strategies.

---

## 🌟 Use Cases

- **Memory Aid:** Instantly recall actionable advice from podcasts you’ve listened to.
- **Niche Retrieval:** Targeted search for neurology, vision, cardio, and fitness topics.
- **Personalized Reminders:** Reinforce key wellness habits as daily check-ins.
- **Research Playground:** Test new RAG and LLM optimizations on real-world data.

---

## 🌱 Future Goals

- **Contextual Memory:** Enhance ability to track multi-turn conversations and longer context.
- **Continuous Knowledge Expansion:** Seamless ingestion of more sources (YouTube, blogs, research).
- **UI/UX:** Expand chatbot into personal website/extension for always-on access.
- **Advanced RAG:** Integrate web search fallback, answer grading, and multi-model generation.

---

## 🤝 Open for Collaboration

If you’re passionate about health tech, RAG, or LLM infra, feel free to fork, open an issue, or reach out!

MIT License

```

```
