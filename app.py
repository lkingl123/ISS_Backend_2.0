from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/initiate_call', methods=['POST'])
def initiate_call():
    try:
        # Extract data from incoming request
        data = request.json
        print("Received data:", data)  # Log the received data

        phone = str(data.get('phone'))  # Convert phone to string
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        # Validate required fields
        if not phone or not first_name or not last_name:
            print("Missing required fields")  # Log missing fields
            return jsonify({"error": "Missing required fields: 'phone', 'firstName', and 'lastName' are required."}), 400

        # Use a predefined prompt ID for testing
        prompt_id = 83249

        # Combine first and last names
        name = f"{first_name} {last_name}"

        # Ensure AIR_API_KEY is set
        air_api_key = os.environ.get('AIR_API_KEY')
        if not air_api_key:
            print("AIR_API_KEY is not set")  # Log missing API key
            return jsonify({"error": "AIR_API_KEY is not set."}), 400

        # Log generated values
        print(f"Using predefined prompt_id: {prompt_id}")
        print(f"Formatted phone: {phone}")
        print(f"Combined name: {name}")

        # AIR API URL
        url = "https://api.air.ai/v1/calls"

        # Prepare the headers and payload for the AIR API request
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {air_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "promptId": prompt_id,
            "phone": phone,
            "name": name,
            "metadata": {}
        }

        # Log the headers and payload
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")

        # Make the POST request to the AIR API
        response = requests.post(url, json=payload, headers=headers)

        # Log the full response details
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        # Check for successful request
        if response.status_code == 200:
            print("Call initiated successfully")  # Log success
            return jsonify({"message": "Call initiated successfully", "promptId": prompt_id}), 200
        else:
            print("Failed to initiate call:", response.text)  # Log failure details
            return jsonify({"error": "Failed to initiate call", "details": response.text}), response.status_code
    except Exception as e:
        print("Exception occurred:", str(e))  # Log any exceptions
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
