import bcrypt
import random
import os
from nanoid import generate
from flask import request, jsonify
from .data import users, padi_datas
from services.store_data import store_user_data, store_prediction_data
from services.inference_service import predict_image
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image

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

def padi_data_handler():
    try:
        # Extract the image file and userId from form-data
        image_file = request.files.get('imageUri')  # 'image' is the key used in form-data
        user_id = request.form.get('userIds')  # 'userIds' is the key for the user ID

        if not image_file:
            return jsonify({
                "status": "fail",
                "message": "Image file is required"
            }), 400

        if not user_id:
            return jsonify({
                "status": "fail",
                "message": "User ID is required"
            }), 400

        # Read the image file into memory (no need to save it to disk)
        img = Image.open(BytesIO(image_file.read()))  # Open the image directly from the byte stream

        # Save image temporarily for prediction (without saving it to disk)
        img_path = "temporary_image.jpg"  # You can ignore saving this to disk as it's just for processing
        img.save(img_path)

        # Predict the result using the loaded model
        result = predict_image(img_path)

        # Prepare the prediction data
        padi_data = {
            "id": user_id,
            "image": img_path,
            "result": result
        }

        # Store the prediction data
        store_prediction_data(user_id, padi_data)

        # Return the success response
        return jsonify({
            "status": "success",
            "message": "Data successfully processed",
            "padiDatas": padi_data
        }), 201

    except Exception as e:
        print(f"Error in padi_data_handler: {e}")
        return jsonify({
            "status": "error",
            "message": "An error occurred while processing the request"
        }), 500

# def padi_data_handler():
#     try:
#         # Extract `imageUri` from the request payload
#         payload = request.get_json()
#         image_uri = payload.get("imageUri")
#         user_id = payload.get("userIds")

#         if not image_uri:
#             return jsonify({
#                 "status": "fail",
#                 "message": "Image URI is required"
#             }), 400

#         # Predict the result using the loaded model
#         result = predict_image(image_uri)

#         # Prepare the prediction data
#         padi_data = {
#             "id": user_id,
#             "image": image_uri,
#             "result": result
#         }

#         # Store the prediction data
#         store_prediction_data(user_id, padi_data)

#         # Return the success response
#         return jsonify({
#             "status": "success",
#             "message": "Data successfully processed",
#             "padiDatas": padi_data
#         }), 201

#     except Exception as e:
#         print(f"Error in padi_data_handler: {e}")
#         return jsonify({
#             "status": "error",
#             "message": "An error occurred while processing the request"
#         }), 500


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