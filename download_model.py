# download_model.py
import os
from huggingface_hub import hf_hub_download

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# Define the model repository and filename
repo_id = "Subh775/Threat-Detection-YOLOv8n"
filename = "weights/best.pt"
local_dir = "models"
local_filename = "threat_best.pt"  # The name your project expects

print(f"Downloading {filename} from {repo_id}...")

# Download the model
downloaded_path = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    local_dir=local_dir,
)

# Rename the file to match your project's expectation
downloaded_dir = os.path.dirname(downloaded_path)
target_path = os.path.join(local_dir, local_filename)

if os.path.abspath(downloaded_path) != os.path.abspath(target_path):
    if os.path.exists(target_path):
        os.remove(target_path)
    os.replace(downloaded_path, target_path)

print(f"Model successfully downloaded and saved as: {target_path}")