import bcrypt
import random
from nanoid import generate
from flask import request, jsonify
from .data import users, padi_datas
from services.store_data import store_user_data, store_prediction_data

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
    data = request.get_json()
    user_ids = data.get('userIds')
    image_uri = data.get('imageUri')
    label = request.args.get('label')
    score = request.args.get('score')
    desc = request.args.get('desc')
    cPenanggulangan = request.args.get('cPenanggulangan')
    cMengobati = request.args.get('cMengobati')

    if not user_ids:
        return jsonify({
            'status': 'fail', 
            'message': 'User tidak ditemukan'
        }), 401
    
    post_id = random.randint(100000, 999999)

    new_padi_data = {
        'id': post_id,
        'userIds': user_ids,
        'imageUri': image_uri,
        'label': label,
        'score': score,
        'desc': desc,
        'cPenanggulangan': cPenanggulangan,
        'cMengobati': cMengobati
    }

    if not image_uri:
        return jsonify({
            'status': 'fail', 
            'message': 'Gambar tidak ditemukan'
        }), 401


    padi_datas.append(new_padi_data)
    store_prediction_data(str(post_id), new_padi_data)

    return jsonify({
        'status': 'success',
        'message': 'Data berhasil diterima',
        'post_id': post_id,
        'padiDatas': new_padi_data
    }), 201


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