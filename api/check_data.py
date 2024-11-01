from chromadb import Client
from api.config import VECTOR_DB_NAME

# Initialize the ChromaDB client
client = Client()
collection = client.get_or_create_collection(VECTOR_DB_NAME)

def check_data_existence(category):
    """Check if there is data in ChromaDB for the specified category."""
    # Query the database to check if any documents exist for the specified category
    results = collection.query(
        where={"category": category},
        include=["documents", "metadatas", "ids"]
    )

    if results["documents"] and results["documents"][0]:
        print(f"Documents found for category '{category}':")
        for doc in results["documents"][0]:
            print(doc)
        return True
    else:
        print(f"No documents found for category '{category}'.")
        return False

def check_all_categories(categories):
    """Check data existence for multiple categories."""
    for category in categories:
        exists = check_data_existence(category)
        if not exists:
            print(f"Data missing for category '{category}'. You may need to re-ingest this data.")

if __name__ == "__main__":
    # Define your categories to check, based on your topics
    categories = [
        "Eye Health", "Neuro", "Cancer Prevention",
        "Strength and Weights Training", "Fat Loss",
        "Random Advice", "Quick Tips"
    ]
    check_all_categories(categories)
