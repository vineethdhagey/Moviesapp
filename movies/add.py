from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# Connect to MongoDB container on port 27018
client = MongoClient("mongodb://movies-mongo-new:27017/")
db = client["moviesappdb"]
movies_collection = db["movies"]

# ----------------- CREATE -----------------
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.json
    user_id = data['user_id']
    title = data.get('movie')
    year = data.get('year')
    genre = data.get('genre')
    rating = data.get('rating')
    favorite = data.get('favorite', False)  # Default is regular movie

    movie_doc = {
        "user_id": user_id,
        "title": title,
        "year": year,
        "genre": genre,
        "rating": rating,
        "favorite": favorite
    }

    result = movies_collection.insert_one(movie_doc)
    return jsonify({"message": f"Movie '{title}' added!", "_id": str(result.inserted_id)}), 201

# ----------------- READ -----------------
@app.route('/movies/<user_id>', methods=['GET'])
def get_movies(user_id):
    movies = movies_collection.find({"user_id": user_id})
    movie_list = []
    for m in movies:
        movie_list.append({
            "_id": str(m["_id"]),
            "title": m["title"],
            "year": m.get("year"),
            "genre": m.get("genre"),
            "rating": m.get("rating"),
            "favorite": m.get("favorite", False)
        })
    return jsonify({"movies": movie_list}), 200

# ----------------- DELETE -----------------
@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        result = movies_collection.delete_one({"_id": ObjectId(movie_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Movie not found"}), 404
        return jsonify({"message": "Movie deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
