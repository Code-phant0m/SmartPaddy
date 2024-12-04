import os
import requests
from dotenv import load_dotenv
from tensorflow.keras.models import load_model

load_dotenv()

MODEL_PATH = "./saved_model/model.h5"

def download_model():
    model_url = os.getenv("MODEL_URLV2")
    if not model_url:
        raise ValueError("MODEL_URL is not defined in the .env file")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    try:
        response = requests.get(model_url, stream=True)
        if response.status_code == 200:
            with open(MODEL_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Model downloaded successfully")

        else:
            raise Exception(f"Failed to download model. HTTP Status: {response.status_code}")
    
    except Exception as e:
        print(f"Error during model download: {e}")
        raise e


def load_model_from_env():
    """Load the model into memory, downloading if necessary."""
    if not os.path.exists(MODEL_PATH):
        print("Model not found locally. Downloading...")
        download_model()
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e
