from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient
import requests
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

CORS(app)

# Azure configurations
BLOB_STORAGE_CONNECTION_STRING = "CONNECTION STRING"
TRANSLATOR_API_KEY = "API KEY"
TRANSLATOR_ENDPOINT = "ENDPOINT"
REGION = "REGION"

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
container_name = "totraduploads"  # Your Blob Storage container name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file and target language
        file = request.files['file']
        language = request.form['language']

        # Read file content
        file_content = file.read().decode('utf-8')

        # Reset file pointer and upload to Blob Storage
        file.seek(0)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(file, overwrite=True)

        # Translate the text
        translation = translate_text(file_content, language)
        if not translation:
            return jsonify({"error": "Translation failed. Please try again."}), 500

        # Save the translated text to Blob Storage
        translated_filename = f"translated_{file.filename}"
        translated_blob_client = blob_service_client.get_blob_client(container=container_name, blob=translated_filename)
        translated_blob_client.upload_blob(translation, overwrite=True)

        # Return the translated file link
        return jsonify({
            "message": "File translated successfully!",
            "translated_file_url": translated_blob_client.url
        })
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def translate_text(text, language):
    try:
        # Call Azure Translator API
        endpoint = f"{TRANSLATOR_ENDPOINT}/translate"
        headers = {
            "Ocp-Apim-Subscription-Key": TRANSLATOR_API_KEY,
            "Ocp-Apim-Subscription-Region": REGION,
            "Content-Type": "application/json"
        }
        params = {"api-version": "3.0", "to": language}
        body = [{"text": text}]

        response = requests.post(endpoint, headers=headers, params=params, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors

        response_data = response.json()
        return response_data[0]['translations'][0]['text']
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors
        if e.response.status_code == 401:
            print("Unauthorized: Please check your API key and endpoint.")
        else:
            print(f"HTTPError: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions
        print(f"RequestException: {e}")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
