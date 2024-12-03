import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Path ke model yang sudah diunduh secara manual
model_local_path = 'D:/Bangkit 2024 - SIB/SmartPaddy_final_.h5'

# Load model dari path lokal
model = load_model(model_local_path)

# Cek input shape model yang diharapkan
print("Expected model input shape:", model.input_shape)

# Path ke gambar yang akan diuji
img_path = '../image-plant/healthy_1.jpg'

# Load dan proses gambar
img = image.load_img(img_path, target_size=(256, 256))  # Ukuran gambar disesuaikan dengan input model
plt.imshow(img)
plt.axis('off')  # Sembunyikan axis
plt.show()

# Convert gambar menjadi array
x = image.img_to_array(img)

# Normalisasi gambar ke rentang [0, 1] jika model memerlukannya
x = x / 255.0  # Skala nilai piksel (periksa apakah ini sesuai dengan proses pelatihan model)

# Sesuaikan bentuk input jika diperlukan (periksa apakah model mengharapkan input 1D atau 2D)
if len(model.input_shape) == 2:  # Untuk model yang mengharapkan input ter-flatten
    x = x.flatten()
    x = np.expand_dims(x, axis=0)  # Tambahkan dimensi batch
elif len(model.input_shape) == 4:  # Untuk model yang mengharapkan gambar 2D
    x = np.expand_dims(x, axis=0)  # Tambahkan dimensi batch

# Lakukan prediksi
classes = model.predict(x)

# Definisikan nama kelas
class_names = ['blast', 'blight', 'brown spot', 'healthy', 'hispa', 'tungro']

# Ambil kelas yang diprediksi dan probabilitasnya
predicted_class = class_names[np.argmax(classes)]
predicted_prob = np.max(classes)

# Tampilkan hasil
print(f"Predicted Class: {predicted_class}")
print(f"Probability: {predicted_prob:.2f}")
