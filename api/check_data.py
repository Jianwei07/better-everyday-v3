from config import collection

def check_all_data():
    # Retrieve all documents to check if data exists
    results = collection.get(include=["documents", "metadatas"])
    print("All data in collection:", results)

    if not results.get("documents") or not results["documents"]:
        print("No data found in the collection.")
    else:
        print("Data exists in the collection.")
        for doc, metadata in zip(results["documents"], results["metadatas"]):
            print("Document:", doc)
            print("Metadata:", metadata)
            print("--------")

if __name__ == "__main__":
    print("Checking collection name:", collection.name)
    check_all_data()
