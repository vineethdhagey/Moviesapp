from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import requests
import os

app = Flask(__name__)
CORS(app)

# -------------------- MONGODB --------------------
# Connect to MongoDB container on a different port (27018)
client = MongoClient("mongodb://movies-mongo-new:27017/")
db = client["moviesappdb"]
users_collection = db["users"]

# -------------------- MOVIE SERVICE --------------------
MOVIE_SERVICE_URL = "http://movie-service:5001"


# -------------------- FRONTEND --------------------
@app.route('/')
def serve_frontend():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.dirname(__file__), path)

# -------------------- AUTH --------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400
    result = users_collection.insert_one({"username": username, "password": password})
    return jsonify({"status": "success", "user_id": str(result.inserted_id), "username": username}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return jsonify({"status": "success", "user_id": str(user["_id"]), "username": username}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# -------------------- MOVIE PROXY --------------------
@app.route('/api/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    user_id = data.get("user_id")
    try:
        response = requests.post(f"{MOVIE_SERVICE_URL}/movies",
                                 json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error connecting to Movie Service: {str(e)}"}), 500

@app.route('/api/movies/<user_id>', methods=['GET'])
def get_movies(user_id):
    try:
        response = requests.get(f"{MOVIE_SERVICE_URL}/movies/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error connecting to Movie Service: {str(e)}"}), 500

@app.route('/api/user_stats/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    try:
        response = requests.get(f"{MOVIE_SERVICE_URL}/user_stats/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error fetching user stats: {str(e)}"}), 500

@app.route('/api/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        response = requests.delete(f"{MOVIE_SERVICE_URL}/movies/{movie_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error deleting movie: {str(e)}"}), 500


# -------------------- MAIN --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
