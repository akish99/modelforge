# import requests
# import numpy as np
# from PIL import Image
# import io

# # --- Configuration ---
# # IMPORTANT: Replace with your actual OpenWeatherMap API key
# WEATHER_API_KEY = "fa8d5fab4c69638fdcae50ae997a35d7"
# WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
# # Coordinates for Mumbai
# MUMBAI_LAT = 19.0760
# MUMBAI_LON = 72.8777

# # IMPORTANT: Update this dictionary with your actual class names from the training script output
# CLASS_NAMES = {
#     0: 'Tomato___Bacterial_spot',
#     1: 'Tomato___Early_blight',
#     2: 'Tomato___healthy',
#     # Add all your other classes here...
# }

# # --- Image Preprocessing ---
# def preprocess_image(image_bytes):
#     """Preprocesses the image for model prediction."""
#     img = Image.open(io.BytesIO(image_bytes))
#     img = img.resize((224, 224))
#     img_array = np.array(img)
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     img_array = img_array / 255.0  # Rescale
#     return img_array

# # --- Plant Care Information ---
# def get_treatment_info(predicted_class):
#     """Returns organic treatment suggestions based on the predicted class."""
#     plant, disease = predicted_class.split('___')
    
#     treatments = {
#         "Bacterial_spot": "Apply copper-based fungicides. Ensure good air circulation and avoid overhead watering.",
#         "Early_blight": "Remove affected lower leaves. Apply a bio-fungicide containing Bacillus subtilis. Mulch the soil.",
#         "Late_blight": "This is serious. Remove and destroy affected plants. Apply copper fungicide preventatively.",
#         "healthy": "Your plant looks healthy! Keep up the good work. Ensure consistent watering and proper nutrients."
#         # Add more disease treatments here
#     }
    
#     return {
#         "plant": plant.replace('_', ' '),
#         "disease": disease.replace('_', ' '),
#         "treatment": treatments.get(disease, "No specific treatment information available.")
#     }

# # --- Weather-based Advice ---
# def get_weather_advice(plant):
#     """Fetches weather data and provides watering advice."""
#     # if WEATHER_API_KEY == "fa8d5fab4c69638fdcae50ae997a35d7":
#     #     return "Weather API key not configured. Cannot provide watering advice."
        
#     try:
#         params = {
#             'lat': MUMBAI_LAT,
#             'lon': MUMBAI_LON,
#             'appid': WEATHER_API_KEY,
#             'units': 'metric'
#         }
#         response = requests.get(WEATHER_API_URL, params=params)
#         response.raise_for_status() # Raise an exception for bad status codes
#         data = response.json()
        
#         temp = data['main']['temp']
#         humidity = data['main']['humidity']
        
#         advice = f"Current weather in Mumbai: {temp}°C, {humidity}% humidity. "
        
#         if temp > 32:
#             advice += "It's very hot. Check soil moisture and consider watering in the evening."
#         elif humidity > 85:
#             advice += "High humidity increases fungal risk. Ensure good air circulation and avoid wetting leaves."
#         else:
#             advice += "Weather seems balanced. Water based on your plant's specific needs."
            
#         return advice

#     except requests.exceptions.RequestException as e:
#         return f"Could not fetch weather data: {e}"

import google.generativeai as genai
from PIL import Image
import io
import os
import json

def get_gemini_diagnosis(image_bytes):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        return json.dumps({"error": "GOOGLE_API_KEY is not configured."})

    genai.configure(api_key=GOOGLE_API_KEY)

    try:
        image = Image.open(io.BytesIO(image_bytes))
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = (
            "You are an expert plant pathologist. Analyze this image of a plant leaf. "
            "Your response must be a single JSON object. Do not include any text or formatting before or after the JSON object. "
            "The JSON object must have the following keys: "
            "'plant_name' (string), "
            "'health_status' (string, e.g., 'Healthy', 'Diseased'), "
            "'diagnosis_details' (string, name of the disease or pest), "
            "'organic_treatment' (string, detailed step-by-step suggestions), "
            "'watering_advice' (string, based on a hot, humid climate like Mumbai)."
        )

        response = model.generate_content([prompt, image])

        json_text = response.text.replace("```json", "").replace("```", "").strip()
        json.loads(json_text)  # validation

        return json_text   # <-- MUST be indented here inside try

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return json.dumps({"error": f"An error occurred while communicating with the AI model: {e}"})
