from flask import Flask, request, jsonify
import json
import os
from pymongo import MongoClient

MONGO_DB_URI = os.environ.get('MONGO_DB_URI')
client = MongoClient(MONGO_DB_URI)
db = client["myDatabase"]
collection = db["users"]  # adjust as needed

app = Flask(__name__)

DATA_FILE = 'data.json'
@app.route('/')
def home():
    return "Flask backend is running!"

@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data received"}), 400

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump([], f)

        with open(DATA_FILE, 'r') as f:
            existing_data = json.load(f)

        existing_data.append(data)

        with open(DATA_FILE, 'w') as f:
            json.dump(existing_data, f, indent=4)

        return jsonify({"message": "Data submitted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
