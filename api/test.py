# import requests
# import os
# from config import HF_TOKEN

# headers = {"Authorization": HF_TOKEN}
# response = requests.get("https://api-inference.huggingface.co/models/google/gemma-2-2b", headers=headers)

# if response.status_code == 200:
#     print("Access granted:", response.json())
# elif response.status_code == 403:
#     print("Access denied:", response.json())
# else:
#     print("Unexpected error:", response.status_code, response.json())
import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
print("Python Path:", sys.path)