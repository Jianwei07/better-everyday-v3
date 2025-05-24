import argparse
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME, CHROMA_PATH
import os
import shutil

def load_documents(data_path):
    loader = DirectoryLoader(
        data_path,
        glob="*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )
    documents = loader.load()
    print(f"[INFO] Loaded {len(documents)} documents from {data_path}")
    return documents

def split_text(documents, chunk_size, chunk_overlap, category):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    for chunk in chunks:
        chunk.metadata["category"] = category.strip().lower()
    print(f"[INFO] Split {len(documents)} documents into {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap}) [category: {category}]")
    chunk_lengths = [len(c.page_content) for c in chunks]
    print(f"[STATS] Chunk sizes: min={min(chunk_lengths)}, max={max(chunk_lengths)}, avg={sum(chunk_lengths)//len(chunk_lengths)}")
    if chunks:
        print(f"[SAMPLE] Chunk content (first chunk): {chunks[0].page_content[:250]}...")
        print(f"[SAMPLE] Chunk metadata: {chunks[0].metadata}")
    print("\n[DEBUG] First 5 chunk metadatas for verification:")
    for i, chunk in enumerate(chunks[:5]):
        print(f"  Chunk {i}: {chunk.metadata}")
    return chunks

def save_to_chroma(chunks, reset_db=False):
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    if reset_db and os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"[INFO] Deleted existing Chroma DB at {CHROMA_PATH}")
        db = Chroma.from_documents(
            chunks, embedding_function, persist_directory=CHROMA_PATH
        )
        print(f"[INFO] Created new Chroma DB with {len(chunks)} chunks.")
    else:
        if os.path.exists(CHROMA_PATH):
            db = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=embedding_function,
            )
            print("[INFO] Loaded existing Chroma DB.")
            db.add_documents(chunks)
            print(f"[INFO] Added {len(chunks)} new chunks to {CHROMA_PATH}.")
        else:
            db = Chroma.from_documents(
                chunks, embedding_function, persist_directory=CHROMA_PATH
            )
            print(f"[INFO] Created new Chroma DB with {len(chunks)} chunks.")
    db.persist()

def main():
    parser = argparse.ArgumentParser(description="Ingest and append to unified ChromaDB with per-chunk category metadata.")
    parser.add_argument("--chunk_size", type=int, default=300)
    parser.add_argument("--chunk_overlap", type=int, default=100)
    parser.add_argument("--data_path", type=str, default="data/neuro")
    parser.add_argument("--category", type=str, required=True, help="Category to tag all chunks with (e.g. neuro, fitness, psychology, general advice)")
    parser.add_argument("--reset_db", action="store_true", help="If set, deletes and recreates ChromaDB from scratch.")
    args = parser.parse_args()

    print(f"\n[RUNNING] Ingesting data from {args.data_path} with chunk_size={args.chunk_size}, chunk_overlap={args.chunk_overlap}, category={args.category}\n")
    documents = load_documents(args.data_path)
    chunks = split_text(documents, args.chunk_size, args.chunk_overlap, args.category)
    save_to_chroma(chunks, reset_db=args.reset_db)

if __name__ == "__main__":
    main()
