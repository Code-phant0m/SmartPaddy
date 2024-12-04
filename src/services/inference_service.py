import numpy as np
from tensorflow.keras.preprocessing import image

# Class dari semua jenis penyakit
class_names = ['blast', 'blight', 'brown spot', 'healthy', 'hispa', 'tungro']
penjelasan = [

]
c_menangani = [
    
]

def predict_image(imageUrl, model):
    try:
        # Load and preprocess gambar untuk menyesuaikan dengan model
        img = image.load_img(imageUrl, target_size=(256, 256))  
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)  # mengubah batch dimension (shape becomes (1, 256, 256, 3)) 

        # Predict the class
        predictions = model.predict(x)
        predicted_class = class_names[np.argmax(predictions)]
        predicted_prob = np.max(predictions)

        # Mengkonversi hasil menjadi readable
        result = {
            "predicted_class": predicted_class,
            "predicted_prob": float(predicted_prob),  
        }

        return result

    except Exception as e:
        print(f"Error during inference: {e}")
        raise e
