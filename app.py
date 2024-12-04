from flask import Flask, request, jsonify
from src.server.routes import register_routes
from src.services.load_model import load_model_from_env

def create_app():

    app = Flask(__name__)

    # Load the model and store it in config (only once)
    if 'MODEL' not in app.config:
        try:
            app.config['MODEL'] = load_model_from_env()
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            return None

    # Register routes
    register_routes(app)

    if __name__ == '__main__':
        app.run(port=5000, host='localhost')

    return app