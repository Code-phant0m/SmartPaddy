import os
import requests
from tensorflow.keras.models import load_model
from tempfile import NamedTemporaryFile

def load_model_from_env():
    try:
        # Get the model URL from the environment variable
        model_url = os.getenv("MODEL_URL")
        if not model_url:
            raise ValueError("MODEL_URL environment variable is not set")
        
        # Download the model file
        response = requests.get(model_url)
        if response.status_code == 200:
            # Create a temporary file to store the downloaded model
            with NamedTemporaryFile(delete=False, suffix='.h5') as temp_file:
                temp_file.write(response.content)
                model_path = temp_file.name
                print(f"Model downloaded and saved to: {model_path}")

                # Load the model from the local temporary file
                model = load_model(model_path)
                print("Model successfully loaded")
                return model
        else:
            raise Exception(f"Failed to download model. HTTP status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e
