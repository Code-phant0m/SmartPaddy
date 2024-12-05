# SmartPaddy API Guides :

@app.route('/register', methods=['POST'])
def register():
    return regis_user_handler()

@app.route('/login', methods=['POST'])
def login():
    return login_user_handler()

## Routes untuk melakukan proses Scan gambar tanaman padi
@app.route('/scan', methods=['POST'])
def scan():
    return padi_data_predict()

## Expected input :
- Image : Variable gambar berupa .png / .jpg
- UserId : Variable string yang berfungsi untuk autentikasi

## Expected Output :
Case 1 ( Jika Gambar dan UserId ada dan berhasil diterima ) : code 200
  {
    "data": {
        "predict_id": "String",
        "result": {
            "c_menangani": "String",
            "gejala": "String",
            "penjelasan": "String",
            "predicted_class": "String",
            "predicted_prob": Float
        },
        "user_id": "String"
    },
    "status": "success"
}

Case 2 ( Jika Gambar tidak disediakan ) : code 400
  {
    "message": "Image file is required",
    "status": "fail"
  }

Case 3 ( Jika UserId tidak disediakan ) : code 400
  {
    "message": "User ID is required",
    "status": "fail"
  }

Case 4 ( Jika Gambar tidak valid / bukan gambar padi ) : 
  Lagi dalam proses pengembangan

@app.route('/post/<string:post_id>', methods=['GET'])
def post_detail(post_id):
    return get_post_detail(post_id)

@app.route('/history/<string:user_id>', methods=['GET'])
def history(user_id):
    return get_history(user_id)
