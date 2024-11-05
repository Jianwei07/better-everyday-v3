# add_data.py
from sentence_transformers import SentenceTransformer
from api.config import EMBEDDING_MODEL_NAME,collection

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def add_data_with_metadata(texts, category):
    embeddings = embedding_model.encode(texts)
    ids = [f"{category}_text_{i}" for i in range(len(texts))]
    metadatas = [{"category": category, "text": text} for text in texts]

    collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
    print(f"Added {len(texts)} items to the '{category}' category.")

    # Check contents immediately after addition
    results = collection.get(include=["documents", "metadatas"])
    print("Data in collection after addition:", results)

# Define health advice data for each topic
eye_health_advice = [
    "Reduce screen time to avoid eye strain.",
    "Take frequent breaks when working on a computer.",
    "Use the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds."
]

neuro_health_advice = [
    "Engage in regular mental exercises like puzzles or reading.",
    "Get sufficient sleep to support cognitive function.",
    "Include omega-3 fatty acids in your diet for brain health."
]

cancer_prevention_advice = [
    "Eat a balanced diet rich in fruits and vegetables.",
    "Avoid smoking and limit alcohol consumption.",
    "Engage in regular physical activity to maintain a healthy weight."
]

strength_training_advice = [
    "Warm up properly before lifting weights.",
    "Focus on form, not just weight, to avoid injury.",
    "Incorporate compound movements like squats and deadlifts."
]

fat_loss_advice = [
    "Maintain a calorie deficit to lose fat.",
    "Incorporate both cardio and strength training in your routine.",
    "Eat a high-protein diet to retain muscle mass while losing fat."
]

random_advice = [
    "Stay hydrated throughout the day for optimal health.",
    "Get 7-8 hours of sleep each night.",
    "Practice mindfulness to reduce stress."
]

quick_tips = [
    "Take a deep breath and relax!",
    "Drink a glass of water.",
    "Stand up and stretch if you’ve been sitting for a while."
]

# Add data to the database for each topic
if __name__ == "__main__":
    add_data_with_metadata(eye_health_advice, "Eye Health")
    add_data_with_metadata(neuro_health_advice, "Neuro")
    add_data_with_metadata(cancer_prevention_advice, "Cancer Prevention")
    add_data_with_metadata(strength_training_advice, "Strength and Weights Training")
    add_data_with_metadata(fat_loss_advice, "Fat Loss")
    add_data_with_metadata(random_advice, "Random Advice")
    add_data_with_metadata(quick_tips, "Quick Tips")
    print("All health data added to the vector database.")
