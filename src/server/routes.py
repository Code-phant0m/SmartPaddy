from flask import Flask
from .handler import regis_user_handler, login_user_handler, padi_data_handler, get_post_detail, get_history

def register_routes(app: Flask):
    
    @app.route('/register', methods=['POST'])
    def register():
        return regis_user_handler()

    @app.route('/login', methods=['POST'])
    def login():
        return login_user_handler()

    @app.route('/scan', methods=['POST'])
    def scan():
        return padi_data_handler()

    @app.route('/post/<string:post_id>', methods=['GET'])
    def post_detail(post_id):
        return get_post_detail(post_id)

    @app.route('/history/<string:user_id>', methods=['GET'])
    def history(user_id):
        return get_history(user_id)