import bcrypt
import os
from nanoid import generate
from flask import request, jsonify, current_app
from io import BytesIO
from .data import users, padi_datas
from src.services.store_data import store_user_data, store_prediction_data, get_prediction_data
from src.services.inference_service import predict_image
from google.cloud import firestore
from werkzeug.utils import secure_filename
from datetime import datetime

def regis_user_handler():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'status': 'fail', 'message': 'Mohon isi seluruh data'}), 400

    if any(user['email'] == email for user in users):
        return jsonify({'status': 'fail', 'message': 'Email sudah terdaftar'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    token = generate(size=16)
    
    new_user = {
        'token': token,
        'name': name,
        'email': email,
        'password': hashed_password
    }
    
    users.append(new_user)
    store_user_data(new_user)
    
    return jsonify({
        'status': 'success',
        'message': 'User berhasil ditambahkan',
        'user': {'token': token, 'name': name, 'email': email}
    }), 201

def login_user_handler():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'status': 'fail', 'message': 'Mohon isi email dan password'}), 400

    user = next((user for user in users if user['email'] == email), None)
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'status': 'fail', 'message': 'Email atau password salah'}), 401

    return jsonify({
        'status': 'success',
        'token': user['token'],
        'message': 'Selamat datang di SmartPaddy'
    }), 200

def padi_data_predict():
    model = current_app.config['MODEL']

    image_file = request.files.get('imageUri')
    user_id = request.form.get('userIds')
    predict_id = generate(size=16)

    if not image_file:
        return jsonify({"status": "fail", "message": "Image file is required"}), 400
    if not user_id:
        return jsonify({"status": "fail", "message": "User ID is required"}), 400

    try:
        image_stream = BytesIO(image_file.read())
        result = predict_image(image_stream, model)
        created_at = datetime.utcnow()

        padi_data = {
            "user_id": user_id,
            "created_at": created_at,
            "predict_id": predict_id,
            "result": result
        }

        store_prediction_data(predict_id, padi_data)

        return jsonify({"status": "success", "data": padi_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def append_prediction_data(predict_id, padi_data):
    padi_datas.append(padi_data)

def get_post_detail(predict_id):
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
            "result": data['result']
        } for data in history]

        return jsonify({'status': 'success', 'data': response_history}), 200

    return jsonify({'status': 'fail', 'message': 'History tidak ditemukan'}), 404
