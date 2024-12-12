import numpy as np
from tensorflow.keras.preprocessing import image

# Class dari semua jenis penyakit
class_names = ['blast', 'blight', 'brown spot', 'hispa', 'tungro', 'healthy']
penjelasan = [
    'Penyakit Blast(Blas) adalah penyakit yang disebabkan oleh jamur Pyricularia oryzae. Jamur ini dapat menginfeksi pada semua fase pertumbuhan tanaman padi mulai dari persemaian sampai menjelang panen.',
    'Penyakit Blight atau Hawar Daun (Bacterial Leaf Blight) adalah penyakit yang disebabkan oleh bakteri Xanthomonas campestris pv. oryzae (Xoo). Penyakit hawar daun ini disebabkan oleh patogen yang menginfeksi daun padi pada semua fase pertumbuhan tanaman, mulai dari pesemaian sampai menjelang panen. Tingkat kerusakan bervariasi antara 15-80%, bergantung pada tingkat serangan.',
    'Penyakit (Brown Spot) atau bercak coklat pada padi adalah penyakit yang disebabkan oleh jamur Cochliobolus miyabeanus  dan ditandai dengan bercak berwarna coklat gelap atau merah-coklat pada daun dan batang padi.',
    'Hispa adalah penyakit pada tanaman padi yang disebabkan oleh serangan serangga Dicladispa armigera, yang dikenal sebagai kumbang Hispa. Serangga ini menyerang daun padi, menyebabkan kerusakan yang terlihat sebagai garis-garis putih akibat penggerekannya.',
    'Tungro merupakan penyakit yang disebabkan oleh infeksi ganda dari 2 jenis virus yang berlainan. Kedua virus yang dimaksud adalah Rice Tungro Spherical Virus (RTSV) dan Rice Tungro Bacilliform Virus (RTBV). Penyakit ini bisa ditularkan oleh beberapa jenis hewan serangga, tetapi yang paling cepat menularkan adalah spesies wereng hijau. Penyebaran penyakit tungro semakin meluas cepat bukan hanya disebabkan oleh kepadatan populasi wereng hijau saja. Penyakit tersebut bisa semakin parah dan ganas karena adanya inokulum tungro atau faktor lainnya. Misalnya, tanaman padi yang sudah terinfeksi virus tungro yang sudah terlanjur ditanam, gulma, singgang, atau yang lainnya. Ada juga penyebab dari perilaku petani itu sendiri saat menanam padi. Misalnya, pemilihan bibit padi yang berkualitas rendah sehingga rentan terserang penyakit, penanaman padi yang tidak serempak, atau bahkan pengaruh musim terutama musim penghujan dengan kelembaban tinggi. Dipastikan serangan wereng hijau akan semakin mengganas jika tidak segera diantisipasi.',
    'Padi Sehat (Healthy) mengacu pada kondisi tanaman padi yang tumbuh optimal tanpa serangan hama atau penyakit. Namun, dalam konteks penyakit, "padi sehat" sering dikaitkan dengan tanaman yang bebas dari berbagai gangguan seperti bakteri, jamur, dan serangga. '
]
gejala = [
    '1. Blas Daun (leaf blast). Adanya bercak berbentuk belah ketupat pada daun, pada bagian tepi bercak berwarna kecoklatan dan pada bagian tengah bercak berwarna putih keabuan.\
     2. Blas leher (node blast). Pada malai terlihat jika ada tangkai malai yang membusuk/ blas leher yang menyebabkan gabah hampa jika serangan terjadi sebelum masa pengisian bulir. Infeksi pada batang menyebabkan batang busuk dan mudah patah bila terhembus angin.',

    'Pada awalnya gejala terdapat pada tepi daun atau bagian daun yang luka berupa garis bercak kebasahan, bercak tersebut meluas berwarna hijau keabu-abuan, selanjutnya seluruh daun menjadi keriput dan kering akhirnya layu. Bagian yang kering ini akan semakin meluas ke arah tulang daun hingga seluruh daun akan mengering. Serangan oleh bakteri ini dapat terjadi pada fase vegetatif dan generatif yang mengakibatkan kerusakan tanaman serta menurunkan hasil produksi tanaman padi.',

    'Pada daun terdapat bercak-bercak sempit memanjang, berwarna coklat kemerahan, sejajar dengan ibu tulang daun. Banyaknya bercak makin meningkat pada waktu tanaman membentuk anakan. Pada serangan yang berat bercak-bercak terdapat pada upih daun, batang, dan bunga. Pada saat tanaman mulai masak gejala yang berat mulai terlihat pada daun bendera. Gejala mulai tampak 2-4 minggu setelah padi di pindah, dan gejala paling berat tampak lebih kurang satu bulan sebelum panen.',

    '1. Lubang kecil di daun: Daun terlihat berlubang kecil akibat gigitan kumbang dewasa. \
     2. Garis putih memanjang: Larva menyerang jaringan daun, menciptakan garis putih panjang yang dapat melemahkan proses fotosintesis.\
     3. Daun menjadi kering: Kerusakan parah dapat menyebabkan daun menjadi kering dan berwarna cokelat.',

    '1. Perubahan warna pada daun muda tanaman padi yang menguning hingga berwarna jingga. \
     2.Daun-daun tersebut juga terlihat melintir.\
     3. Tanaman padi menjadi kerdil karena jarak antar buku atau ruas memendek.\
     4. Jumlah tanaman padimuda atau anakan menjadi berkurang drastis karena lebih rentan terserang virus tungro',

    'Tanaman padi yang sehat dapat ditandai dengan: Tanaman padi tumbuh subur, bebas dari hama dan penyakit, memiliki daun yang sehat, Batang tanaman padi kokoh, Gabah padi bernas.'
]
c_menangani = [
    '1. Menggunakan varietas unggul yang tahan terhadap penyakit blas,  seperti Inpari 21, Inpari 22, Inpari 26, Inpari 27, Inpago 4, Inpago 5, Inpago 6, Inpago 7, dan Inpago 8.\
     2. Gunakan benih yang sehat.\
     3. Melakukan rotasi varietas. \
     4. Menanam dengan  jarak yang tidak terlalu rapat, untuk mengurangi kelembaban. \
     5. Hindari penggunaan pupuk nitrogen diatas anjuran. Gunakanlah pupuk yang seimbang untuk meningkatkan ketahanan tanaman terhadap penyakit. \
     6. Penyemprotan pestisida sistemik sebanyak 2 kali pada saat stadia tanaman anakan maksimum dan awal berbunga. \
     7. Penyemprotkan fungisida seperti Benomyl 50WP, Mancozeb 80%, Carbendazim 50%, isoprotiolan 40%, dan trisikazole 20%. Penyemprotan sebaiknya dilakukan dua kali, yaitu saat tanaman padi anakan maksimum dan awal berbunga. \
     8. Menggunakan Paenibacillus polymyxa dengan dosis 5 cc/liter air. Pengaplikasianya yakni pada persemaian, umur 2 minggu setelah tanam (MST), 4 MST, 6 MST dan 8 MST. Selain aplikasi di persemaian, paenibacillus juga diaplikasikan pada saat benih belum sebar dengan cara perendaman selama 15 sampai 20 menit. \
     9. Memberikan Mengomposkan jerami sisa panen untuk penyehatan lahan. \
    10. Menjaga kebersihan lingkungan sawah dan gulma yang mungkin menjadi inang alternatif. Anda juga dapat membersihkan sisa-sisa tanaman yang terinfeksi. ',
    
    '1. Perbaikan cara bercocok tanam, melalui: \
        a. Pengolahan tanah secara optimal \
        b. Pengaturan pola tanam dan waktu tanam serempak dalam satu hamparan \
        c. Pergiliran tanam dan varietas tahan \
        d. Penanaman varietas unggul dari benih yang sehat \
        e. Pengaturan jarak tanam \
        f. Pemupukan berimbang (N,P, K dan unsur mikro) sesuai dengan fase pertumbuhan dan musim \
        g. Pengaturan sistem pengairan sesuai dengan fase pertumbuhan tanaman. \
     2. Sanitasi lingkungan \
     3. Pemanfaatan agensia hayati Corynebacterium \
     4. Penyemprotan bakterisida anjuran yang efektif dan diizinkan secara bijaksana berdasarkan hasil pengamatan.',

    '1. Penyemprotan fungisida. Melakukan 3 kali penyemprotan yaitu pada fase anakan maksimum, awal pembungaan dan awal pengisian dengan fungisida benomil, mankozeb, carbendazim, atau difenoconazol dengan dosis 1 cc per 1 liter air, dengan volume semprot 500 liter per ha, dapat menekan perkembangan penyakit bercak daun cercospora dan menekan kehilangan hasil padi sampai dengan 30%. \
     2. Merendam benih dalam air panas (53–54 °C) selama 10–12 menit untuk memastikan benih tidak terkontaminasi. \
     3. Gunakan varietas padi yang tahan terhadap penyakit tersebut jika tersedia di daerah Anda. \
     4. Menyingkirkan gulma dan tanaman liar di lahan dan sekitarnya. \
     5. Memupuk berimbang: Rencanakan pemupukan berimbang sepanjang musim dan pastikan untuk menggunakan kalium yang cukup. \
     6. Menggunakan agens hayati untuk meningkatkan ketahanan tanaman terhadap penyakit. \
     7. Menjaga kelembaban \
     8. Menjaga jarak tanam. Jarak tanam yang lebih lebar dapat mengurangi serangan penyakit. ',

    '1. Gunakan jarak tanam yang lebih rapat dengan kerapatan daun yang lebih besar yang dapat mentoleransi jumlah hispa yang lebih banyak. \
     2. Tanam tanaman di awal musim untuk menghindari populasi puncak. \
     3. Potong ujung pucuk untuk mencegah serangga bertelur. \
     4. Kumpulkan serangga dewasa dengan jaring penyapu, terutama di pagi hari ketika mereka kurang banyak bergerak. \
     5. Singkirkan segala jenis gulma dari sawah selama musim tanpa penanaman. \
     6. Daun dan pucuk yang terserang harus dipotong dan dibakar, atau dikubur dalam di bawah lumpur. \
     7. Hindari pemupukan nitrogen yang berlebihan di ladang yang terserang. \
     8. Lakukan rotasi tanaman untuk memutus siklus hidup hama ini ',

    '1. Menanam padi serempak pada lahan luas minimal 25 hektar. \
     2. Mengatur waktu tanam padi dengan sebaik-baiknya. Saat puncak kepadatan populasi wereng hijau, tanaman padi sudah berumur lebih dari 45 hari setelah tanam, umur tanaman padi yang tidak rentan terhadap penyakit tungro. \
     3. Memilih varietas tanaman padi yang berkualitas bagus, sehingga tidak mudah terserang wereng hijau dan virus tungro. \
     4. Melakukan pemupukan berimbang sesuai dosis yang direkomendasikan dinas pertanian terkait. \
     5. Membasmi virus tungrodan tempat-tempat penyebab perkembangbiakannya, seperti singgang, gulma, bibit tanaman yang sudah terinfeksi penyakit, dan lain sebagainya. \
     6. Menggunakan bahan insektisida pada fase sebelum semai dengan dosis yang masih aman dan direkomendasikan. \
     7. Melakukan pengamatan intensif pada tanaman padi dibantu oleh petugas pengamat hama dan penyakit – pengendali organisme pengganggu tanaman (PHP – POPT). \
     8. Melakukan sosialisasi dan pembelajaran kepada para petani secara umum melalui sekolah lapang pengendalian hama terpadu(SLPHT).',

    '1. Mengendalikan hama: Anda dapat menggunakan pestisida organik untuk mengendalikan hama yang menyerang tanaman padi, seperti tikus, wereng, belalang, dan walang sangit. Anda juga dapat memasang orang-orangan di sawah untuk mengusir burung yang merusak tanaman padi. \
     2. Mengendalikan penyakit: dengan menggunakan fungisida multifungsi untuk mengendalikan penyakit yang disebabkan oleh cendawan patogen, seperti bercak daun, bercak pelepah, dan busuk batang. \
     3. Menggunakan pupuk organik dan kapur pertanian untuk memperbaiki kesuburan tanah. \
     4. Melakukan penyiangan tanaman padi setiap dua minggu sekali. \
     5. Melakukan pengairan yang wajar sesuai kebutuhan untuk mencegah kekeringan. \
     6. Memilih bibit unggul yang tahan terhadap serangan hama. \
     7. Melakukan rotasi tanam dengan cara menyelipkan tanaman palawija di antara tanaman padi untuk mengurangi serangga hama dan penyakit. '
]

def predict_image(imageUrl, model):
    try:
        # Load dan preprocess image untuk menyesuaikan dengan input model
        img = image.load_img(imageUrl, target_size=(256, 256))  
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)  # menambah batch dimension (1, 256, 256, 3)

        # Melakukan prediksi
        predictions = model.predict(x)
        predicted_index = np.argmax(predictions)
        predicted_class = class_names[predicted_index]
        predicted_prob = np.max(predictions)
        float_predicted_prob = float(predicted_prob)

        # Membuat penjelasan, gejala, dan cara menangani sesuai class 
        explanation = penjelasan[predicted_index]
        symptoms = gejala[predicted_index]
        treat = c_menangani[predicted_index]

        # Model akurasi dan threshold
        model_acc = 0.9
        model_threshold = 0.8

        # hasil dibawah threshold
        if float_predicted_prob < model_threshold:
            result = False
            return result

        # hasil dibawah tingkat akurasi tapi diatas threshold
        if model_threshold <= float_predicted_prob < model_acc:
            result = {
                "predicted_class": predicted_class,
                "predicted_prob": float_predicted_prob,
                "message": "Under the model Accuracy", 
                "penjelasan": explanation,
                "gejala": symptoms,
                "c_menangani": treat
            }

            return result

        # hasil ideal
        result = {
            "predicted_class": predicted_class,
            "predicted_prob": float_predicted_prob,
            "penjelasan": explanation,
            "gejala": symptoms,
            "c_menangani": treat
        }

        return result

    except Exception as e:
        print(f"Error during inference: {e}")
        raise e
