import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

class MovieRecommender:
    def __init__(self):
        self.movies_path = "C:/Users/mvdev/Documents/movie-recommendation-system/data/movies.csv"
        self.ratings_path = "C:/Users/mvdev/Documents/movie-recommendation-system/data/ratings.csv"
        
        self.df_movies = None
        self.df_ratings = None
        
        # Content-Based objects
        self.tfidf_matrix = None
        self.content_sim = None
        
        # Collaborative Filtering objects
        self.user_item_matrix = None
        self.item_sim_model = None
        
        self.load_data()
        self.build_content_recommender()
        self.build_collaborative_recommender()

    def load_data(self):
        if not os.path.exists(self.movies_path) or not os.path.exists(self.ratings_path):
            raise FileNotFoundError("Datasets not found. Run generate_data.py first.")
            
        self.df_movies = pd.read_csv(self.movies_path)
        self.df_ratings = pd.read_csv(self.ratings_path)

    def build_content_recommender(self):
        # Clean and preprocess genres: replace '|' with spaces so TF-IDF can vectorize them
        genres_clean = self.df_movies["genres"].str.replace("|", " ", regex=False)
        
        # Vectorize genres
        tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        self.tfidf_matrix = tfidf.fit_transform(genres_clean)
        
        # Compute cosine similarity matrix
        self.content_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def build_collaborative_recommender(self):
        # Create a pivot table: Rows = movies, Columns = users
        # Fill missing ratings with 0
        self.user_item_matrix = self.df_ratings.pivot(
            index="movieId", 
            columns="userId", 
            values="rating"
        ).fillna(0)
        
        # Re-align with all movies in df_movies (some movies might have 0 ratings)
        all_movie_ids = self.df_movies["movieId"].unique()
        self.user_item_matrix = self.user_item_matrix.reindex(all_movie_ids, fill_value=0)
        
        # Fit a k-NN model for Item-Item Collaborative Filtering
        # Using cosine distance to find items that have similar rating patterns across users
        self.item_sim_model = NearestNeighbors(metric="cosine", algorithm="brute")
        self.item_sim_model.fit(self.user_item_matrix.values)

    def get_content_recommendations(self, movie_id, top_n=6):
        # Find index of movie
        idx_list = self.df_movies.index[self.df_movies["movieId"] == movie_id].tolist()
        if not idx_list:
            return []
        idx = idx_list[0]
        
        # Get pairwise similarity scores
        sim_scores = list(enumerate(self.content_sim[idx]))
        
        # Sort by similarity in descending order
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N, excluding the self movie
        recommendations = []
        for index, score in sim_scores:
            row = self.df_movies.iloc[index]
            if row["movieId"] == movie_id:
                continue
            recommendations.append({
                "movieId": int(row["movieId"]),
                "title": row["title"],
                "genres": row["genres"],
                "score": round(float(score), 4)
            })
            if len(recommendations) >= top_n:
                break
                
        return recommendations

    def get_collaborative_recommendations(self, movie_id, top_n=6):
        # Find index in user_item_matrix corresponding to movie_id
        idx_list = self.user_item_matrix.index.get_indexer([movie_id])
        if idx_list[0] == -1:
            # Movie has no ratings or doesn't exist
            return []
        idx = idx_list[0]
        
        # Query the k-NN model
        # Ask for top_n + 1 because the query movie itself will be the closest neighbor (distance = 0)
        distances, indices = self.item_sim_model.kneighbors(
            [self.user_item_matrix.iloc[idx].values], 
            n_neighbors=min(top_n + 1, len(self.user_item_matrix))
        )
        
        distances = distances.squeeze()
        indices = indices.squeeze()
        
        recommendations = []
        for i in range(len(indices)):
            row_idx = indices[i]
            # Convert distance to similarity score
            sim_score = 1 - distances[i]
            
            # Map index back to movieId
            matched_movie_id = self.user_item_matrix.index[row_idx]
            
            if matched_movie_id == movie_id:
                continue
                
            movie_row = self.df_movies[self.df_movies["movieId"] == matched_movie_id].iloc[0]
            recommendations.append({
                "movieId": int(movie_row["movieId"]),
                "title": movie_row["title"],
                "genres": movie_row["genres"],
                "score": round(float(sim_score), 4)
            })
            
            if len(recommendations) >= top_n:
                break
                
        return recommendations

    def get_recommendations(self, movie_id, method="content", top_n=6):
        if method == "content":
            return self.get_content_recommendations(movie_id, top_n)
        elif method == "collaborative":
            return self.get_collaborative_recommendations(movie_id, top_n)
        else:
            raise ValueError(f"Unknown recommendation method: {method}")

if __name__ == "__main__":
    recommender = MovieRecommender()
    print("Testing recommendations for 'The Matrix (199 matrix)' (ID: 1):")
    print("\n--- Content-Based Recommendations ---")
    for r in recommender.get_recommendations(1, method="content", top_n=5):
        print(f"{r['title']} - Genres: {r['genres']} (Score: {r['score']:.4f})")
        
    print("\n--- Collaborative Filtering Recommendations ---")
    for r in recommender.get_recommendations(1, method="collaborative", top_n=5):
        print(f"{r['title']} - Genres: {r['genres']} (Score: {r['score']:.4f})")
