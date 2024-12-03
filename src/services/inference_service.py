import numpy as np
from tensorflow.keras.preprocessing import image
from services.load_model import load_model_from_env

class_names = ['blast', 'blight', 'brown spot', 'healthy', 'hispa', 'tungro']

def predict_image(imageUrl):
    try:
        # Load the model
        model = load_model_from_env()

        # Load and preprocess the image
        img = image.load_img(imageUrl, target_size=(256, 256))  # Resize to 256x256
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)  # Add batch dimension (shape becomes (1, 256, 256, 3))

        # Normalize the image if needed (some models require normalization)
        x = x / 255.0  # Assuming the model was trained with normalized images

        # Predict the class
        predictions = model.predict(x)
        predicted_class = class_names[np.argmax(predictions)]
        predicted_prob = np.max(predictions)

        # Convert to Python-native types for JSON serialization
        result = {
            "predicted_class": predicted_class,
            "predicted_prob": float(predicted_prob),  # Convert to Python float
        }

        return result
    except Exception as e:
        print(f"Error during inference: {e}")
        raise e
