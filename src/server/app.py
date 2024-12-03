from flask import Flask, request, jsonify
from dotenv import load_dotenv
from .routes import register_routes

load_dotenv()

app = Flask(__name__)

register_routes(app)

if __name__ == '__main__':
    app.run(port=5000, host='localhost')