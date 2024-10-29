import requests
import os

hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN_WRITE")

headers = {"Authorization": hf_token}
response = requests.get("https://api-inference.huggingface.co/models/google/gemma-2-2b", headers=headers)

if response.status_code == 200:
    print("Access granted:", response.json())
elif response.status_code == 403:
    print("Access denied:", response.json())
else:
    print("Unexpected error:", response.status_code, response.json())
