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
        json.loads(json_text) 

        return json_text  

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return json.dumps({"error": f"An error occurred while communicating with the AI model: {e}"})
