import chromadb

def main():
    client = chromadb.PersistentClient(path="./chroma_storage")  # Adjust path as needed

    collections = client.list_collections()
    print(f"Collections found: {[c.name for c in collections]}")
    if not collections:
        print("No collections found. Exiting.")
        return

    collection_name = collections[0].name
    print(f"Using collection: {collection_name}")
    collection = client.get_collection(name=collection_name)

    print("\nFetching up to 20 documents (for inspection)...\n")
    results = collection.get(
        limit=20,
        include=["documents", "metadatas"]
    )

    if not results["ids"]:
        print("No documents found in this collection.")
        return

    for i, (doc, meta, doc_id) in enumerate(zip(
        results["documents"],
        results["metadatas"],
        results["ids"]
    )):
        print(f"Doc {i+1} [ID: {doc_id}]:")
        print(f"  Metadata: {meta}")
        print(f"  Document: {doc[:100]}{'...' if len(doc)>100 else ''}")
        print("")

    print("Docs with category 'neuro':")
    neuro_docs = collection.get(
        where={"category": "neuro"},
        include=["metadatas"]
    )
    for i, (meta, doc_id) in enumerate(zip(neuro_docs["metadatas"], neuro_docs["ids"])):
        print(f"  [{doc_id}] {meta}")
        
    # Assuming you already have `collection`
    result = collection.query(
        query_texts=["Who is Steve?"],
        n_results=5,
        include=["documents", "metadatas"]
    )
    print(result)

if __name__ == "__main__":
    main()
