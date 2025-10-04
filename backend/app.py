# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from utils import preprocess_image, get_treatment_info, get_weather_advice, CLASS_NAMES

# # --- Initialization ---
# app = Flask(__name__)
# CORS(app) # Allow cross-origin requests

# # Load the trained model
# try:
#     model = tf.keras.models.load_model('model/plant_disease_model.h5')
#     print("Model loaded successfully!")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     model = None

# # --- API Endpoint ---
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model is not loaded'}), 500
        
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
        
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     try:
#         # Read and preprocess the image
#         img_bytes = file.read()
#         processed_image = preprocess_image(img_bytes)

#         # Make prediction
#         prediction = model.predict(processed_image)
#         predicted_class_index = np.argmax(prediction, axis=1)[0]
#         predicted_class_name = CLASS_NAMES.get(predicted_class_index, "Unknown")
#         confidence = float(np.max(prediction))

#         # Get care information
#         care_info = get_treatment_info(predicted_class_name)
#         watering_advice = get_weather_advice(care_info['plant'])

#         # Prepare response
#         response = {
#             'plant': care_info['plant'],
#             'disease': care_info['disease'],
#             'treatment': care_info['treatment'],
#             'watering_advice': watering_advice,
#             'confidence': f"{confidence:.2%}"
#         }
        
#         return jsonify(response)

#     except Exception as e:
#         print(f"Prediction error: {e}")
#         return jsonify({'error': 'Failed to process the image'}), 500

# # --- Run the App ---
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import init_db, add_user, authenticate_user  # 🔑 Database logic
from utils import get_gemini_diagnosis
import json
import google.generativeai as genai
import os

# --- Load environment variables ---
load_dotenv()

# --- Initialize Flask app ---
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# --- Prediction Endpoint (/predict) ---
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


# --- Authentication Endpoints ---
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


# --- Start the App ---
if __name__ == '__main__':
    init_db()  # 🧱 Initialize the database (create if not exists)

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    print("\n🔍 Available Gemini models:")
    for m in genai.list_models():
        print("-", m.name, "supports:", m.supported_generation_methods)

    app.run(debug=True)
