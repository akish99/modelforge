
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import init_db, add_user, authenticate_user  
from utils import get_gemini_diagnosis
import json
import google.generativeai as genai
import os

load_dotenv()

app = Flask(__name__)
CORS(app) 
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img_bytes = file.read()
        diagnosis_json_string = get_gemini_diagnosis(img_bytes)
        diagnosis_data = json.loads(diagnosis_json_string)

        if 'error' in diagnosis_data:
            return jsonify(diagnosis_data), 500

        return jsonify(diagnosis_data)

    except Exception as e:
        print(f"Error in /predict endpoint: {e}")
        return jsonify({'error': f'Failed to process request: {e}'}), 500


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if add_user(name, email, password):
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'message': 'Email already registered'}), 409


@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = authenticate_user(email, password)
    if user:
        return jsonify({'name': user[0], 'email': user[1]}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    init_db()  

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    print("\n🔍 Available Gemini models:")
    for m in genai.list_models():
        print("-", m.name, "supports:", m.supported_generation_methods)

    app.run(debug=True)
