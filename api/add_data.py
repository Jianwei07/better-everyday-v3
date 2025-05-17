from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from api.config import EMBEDDING_MODEL_NAME
import os
import shutil

CHROMA_PATH = "chroma_storage"
DATA_PATH = "data/neuro"

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    loader = DirectoryLoader(
        "data/neuro",
        glob="*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")  # Explicit encoding
    )
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10] if len(chunks) > 10 else chunks[0]
    print(document.page_content)
    print(document.metadata)
    return chunks

def save_to_chroma(chunks):
    # Clear out the database first.
    # if os.path.exists(CHROMA_PATH):
    #     shutil.rmtree(CHROMA_PATH)

    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    if os.path.exists(CHROMA_PATH):
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function,
        )
        print("Loaded existing Chroma DB.")
        db.add_documents(chunks)
        print(f"Added {len(chunks)} new chunks to {CHROMA_PATH}.")
    else:
        db = Chroma.from_documents(
            chunks, embedding_function, persist_directory=CHROMA_PATH
        )
        print("Created new Chroma DB with these chunks.")
    db.persist()

if __name__ == "__main__":
    main()
