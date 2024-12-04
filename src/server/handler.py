import bcrypt
import random
import os
from nanoid import generate
from flask import request, jsonify, current_app
from io import BytesIO
from .data import users, padi_datas
from src.services.store_data import store_user_data, store_prediction_data
from src.services.inference_service import predict_image
from werkzeug.utils import secure_filename

def regis_user_handler():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({
            'status': 'fail', 
            'message': 'Mohon isi seluruh data'
        }), 400

    if any(user['email'] == email for user in users):
        return jsonify({
            'status': 'fail', 
            'message': 'Email sudah terdaftar'
        }), 400

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

    if not email or not password:
        return jsonify({
            'status': 'fail', 
            'message': 'Mohon isi email dan password'
        }), 400

    user = next((user for user in users if user['email'] == email), None)

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({
            'status': 'fail', 
            'message': 'Email atau password salah'
        }), 401

    return jsonify({
        'status': 'success',
        'token': user['token'],
        'message': 'Selamat datang di SmartPaddy'
    }), 200

def padi_data_predict():
    model = current_app.config['MODEL']
    image_file = request.files.get('imageUri')  # 'imageUri' is the key in form-data
    user_id = request.form.get('userIds')  # 'userIds' is the key for the user ID
    predict_id = generate(size=16)

    if not image_file:
        return jsonify({"status": "fail", "message": "Image file is required"}), 400
    if not user_id:
        return jsonify({"status": "fail", "message": "User ID is required"}), 400

    try:
        # Convert FileStorage to BytesIO
        image_stream = BytesIO(image_file.read())

        #Predict the result using model
        result = predict_image(image_stream, model)

        # Prepare the prediction data
        padi_datas = {
            "id": predict_id,
            "user_id": user_id, 
            "result": result
            }

        return jsonify({"status": "success", "data": padi_datas}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def get_post_detail(post_id):
    post_id = int(post_id)
    padi_data = next((data for data in padi_datas if data['id'] == post_id), None)

    if padi_data:
        return jsonify({
            'status': 'success', 
            'data': {
                'imageUri': padi_data.get("imageUri"),
                "label": padi_data.get("label"),
                "score": padi_data.get("score"),
                "desc": padi_data.get("desc"),
                "cPenanggulangan": padi_data.get("cPenanggulangan"),
                "cMengobati": padi_data.get("cMengobati")
            }
        }), 200

    return jsonify({
        'status': 'fail', 
        'message': 'Post tidak ditemukan'
    }), 404


def get_history(user_id):
    history = [data for data in padi_datas if user_id in data['userIds']]

    if history:
        response_history = [{
            "imageUri": data['imageUri'],
            "label": data['label'],
            "score": data['score']
        } for data in history]
        
        return jsonify({
            'status': 'success', 
            'data': response_history
        }), 200
    
    return jsonify({
        'status': 'fail', 
        'message': 'History tidak ditemukan'
    }), 404