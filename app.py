import os
from flask import Flask, render_template, request, jsonify
from models.recommender_model import MovieRecommender

app = Flask(__name__)

# Initialize the recommender engine
recommender = None
try:
    recommender = MovieRecommender()
    print("Movie Recommender engine loaded successfully!")
except Exception as e:
    print(f"Error loading Movie Recommender: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/movies/list", methods=["GET"])
def get_movies():
    if not recommender or recommender.df_movies is None:
        return jsonify({"error": "Recommender data not loaded."}), 500
        
    # Get movies list and sort by title
    movies_list = recommender.df_movies.to_dict(orient="records")
    # Sort alphabetically by title
    movies_list = sorted(movies_list, key=lambda x: x["title"])
    return jsonify(movies_list)

@app.route("/api/movies/recommend", methods=["POST"])
def recommend_movies():
    if not recommender:
        return jsonify({"error": "Recommender engine is offline."}), 500
        
    try:
        data = request.json
        movie_id = data.get("movieId")
        method = data.get("method", "content") # content or collaborative
        top_n = data.get("top_n", 12)
        
        if not movie_id:
            return jsonify({"error": "Missing parameter: movieId"}), 400
            
        movie_id = int(movie_id)
        
        # Verify query movie exists
        query_movie_rows = recommender.df_movies[recommender.df_movies["movieId"] == movie_id]
        if query_movie_rows.empty:
            return jsonify({"error": f"Movie ID {movie_id} not found."}), 404
            
        query_movie = query_movie_rows.iloc[0].to_dict()
        
        # Fetch recommendations
        recommendations = recommender.get_recommendations(movie_id, method=method, top_n=top_n)
        
        return jsonify({
            "query_movie": {
                "movieId": int(query_movie["movieId"]),
                "title": query_movie["title"],
                "genres": query_movie["genres"]
            },
            "method": method,
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
