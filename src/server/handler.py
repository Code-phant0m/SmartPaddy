import bcrypt
import os
import argon2
from argon2.exceptions import VerifyMismatchError
from nanoid import generate
from flask import request, jsonify, current_app
from io import BytesIO
from .data import users
from src.services.store_data import store_user_data, fetch_user_by_email, store_prediction_data, get_prediction_data
from src.services.inference_service import predict_image
from google.cloud import firestore
from werkzeug.utils import secure_filename
from datetime import datetime
from google.cloud import storage

argon_hash = argon2.PasswordHasher()

def regis_user_handler():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email').strip().lower()
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'status': 'fail', 'message': 'Mohon isi seluruh data'}), 400

    if fetch_user_by_email(email):
        return jsonify({'status': 'fail', 'message': 'Email sudah terdaftar'}), 400

    try:
        hashed_password = argon_hash.hash(password.encode('utf-8'))
        user_id = generate(size=16)
    
        new_user = {
            'user_id': user_id,
            'name': name,
            'email': email,
            'hashed_password': hashed_password
        }
    
        store_user_data(new_user)
        
        return jsonify({
            'status': 'success',
            'message': 'User berhasil ditambahkan',
            'user': {'user_id': user_id, 'name': name, 'email': email}
        }), 201
    
    except Exception as e:
         print(f"Error saat registrasi: {e}")
         return jsonify({"status": "error", "message": f"A server-side error occurred"}), 500

def login_user_handler():
    data = request.get_json()
    email = data.get('email').strip().lower()
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'status': 'fail', 'message': 'Mohon isi email dan password'}), 400

    # Fetch user data from Firestore
    user = fetch_user_by_email(email)

    # Check if user exists
    if user is None:
        return jsonify({'status': 'fail', 'message': 'Akun tidak ditemukan!'}), 401

    # Extract the stored hashed password from the user data
    hash_pass = user['hashed_password']

    # Verify the provided password against the stored hashed password
    if not verify_password(hash_pass, password):
        return jsonify({'status': 'fail', 'message': 'Email atau password salah'}), 401

    return jsonify({
        'status': 'success',
        'email': user['email'],
        'name': user['name'],
        'user_id': user['user_id'],
        'message': 'Selamat datang di SmartPaddy'
    }), 200

def verify_password(stored_hash, password):
    try:
        return argon_hash.verify(stored_hash, password.encode())
    except VerifyMismatchError:
        return False
        
def upload_img_to_bucket(bucket_name, image_file, image_filename, predict_id):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # Ensure file extension exists
        if '.' not in image_filename:
            raise ValueError("Format Nama Invalid. Tidak ada extensi format.")

        file_extension = image_filename.split('.')[-1]
        unique_filename = f"{predict_id}.{file_extension}"

        blob = bucket.blob(unique_filename)
        blob.upload_from_file(image_file, content_type=image_file.content_type)

        blob.make_public()

        return blob.public_url

    except Exception as e:
        print(f"Error saat upload ke bucket: {e}")
        raise ValueError("Gagal untuk menyimpan gambar di Cloud Storage.") from e

def padi_data_predict():
    model = current_app.config['MODEL']
    bucket_name = os.getenv("BUCKET_NAME")

    if not bucket_name:
        return jsonify({"status": "error", "message": "Bucket tidak ditemukan"}), 500

    image_file = request.files.get('imageUri')
    user_id = request.form.get('userIds')
    predict_id = generate(size=16)

    # Error Handling 
    if not image_file:
        return jsonify({"status": "fail", "message": "File Image dibutuhkan"}), 400
    if not user_id:
        return jsonify({"status": "fail", "message": "User ID dibutuhkan"}), 400

    try:
        #Handling for prediction data
        image_stream = BytesIO(image_file.read())
        image_stream.seek(0)
        result = predict_image(image_stream, model)

        created_at = datetime.utcnow()

        # Handling for unrecognizeable image
        if result == False:
            return jsonify({"status": "fail", "message": "Gambar tidak jelas. Gunakan Gambar yang lebih baik!"}), 415

        # Handling for uploading image 
        image_file.stream.seek(0)
        image_filename= image_file.filename
        image_url = upload_img_to_bucket(bucket_name, image_file, image_filename, predict_id)

        padi_data = {
            "user_id": user_id,
            "created_at": created_at,
            "predict_id": predict_id,
            "image_url": image_url,
            "result": result
        }

        store_prediction_data(predict_id, padi_data)

        return jsonify({"status": "success", "data": padi_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def get_post_detail(predict_id):
    try:
        padi_data_item = get_prediction_data(predict_id)

        if padi_data_item:
            return jsonify({
                'status': 'success',
                'data': {
                    'result': padi_data_item['result']
                }
            }), 200
        else:
            return jsonify({'status': 'fail', 'message': 'Data tidak ditemukan'}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to fetch prediction data"}), 500

def get_history(user_id):
    db = firestore.Client()
    predictions_ref = db.collection('predictions')
    query = predictions_ref.where('user_id', '==', user_id).stream()

    history = []
    for doc in query:
        history.append(doc.to_dict())

    if history:
        response_history = [{
            "predict_id": data['predict_id'],
            "image_url": data['image_url'],
            "created_at": data['created_at'],
            "result": data['result']
        } for data in history]

        return jsonify({'status': 'success', 'data': response_history}), 200

    return jsonify({'status': 'fail', 'message': 'History tidak ditemukan'}), 404
