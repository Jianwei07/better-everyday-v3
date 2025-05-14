# You can run this script separately to clean up
from huggingface_hub import delete_cached_files

# Delete the large model
delete_cached_files(repo_id="mistralai/Mistral-7B-Instruct-v0.2")