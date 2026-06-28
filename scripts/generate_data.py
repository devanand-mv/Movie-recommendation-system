import os
import numpy as np
import pandas as pd

def generate_movie_dataset():
    # A curated list of popular movies with realistic genres
    movies_data = [
        # Action & Sci-Fi
        (1, "The Matrix (199 matrix)", "Action|Sci-Fi"),
        (2, "Inception (2010)", "Action|Sci-Fi|Thriller"),
        (3, "Interstellar (2014)", "Sci-Fi|Drama|Adventure"),
        (4, "Avatar (2009)", "Action|Adventure|Sci-Fi|Fantasy"),
        (5, "Blade Runner 2049 (2017)", "Sci-Fi|Thriller|Drama"),
        (6, "The Dark Knight (2008)", "Action|Crime|Drama"),
        (7, "The Avengers (2012)", "Action|Adventure|Sci-Fi"),
        (8, "Iron Man (2008)", "Action|Sci-Fi"),
        (9, "Star Wars: Episode IV - A New Hope (1977)", "Action|Adventure|Sci-Fi"),
        (10, "Star Wars: Episode V - The Empire Strikes Back (1980)", "Action|Adventure|Sci-Fi"),
        (11, "Gladiator (2000)", "Action|Drama|Adventure"),
        (12, "Mad Max: Fury Road (2015)", "Action|Adventure|Sci-Fi"),
        (13, "Terminator 2: Judgment Day (1991)", "Action|Sci-Fi"),
        (14, "Logan (2017)", "Action|Sci-Fi|Drama"),
        (15, "Spider-Man: Into the Spider-Verse (2018)", "Action|Adventure|Animation"),
        
        # Drama & Thriller
        (16, "The Shawshank Redemption (1994)", "Drama"),
        (17, "The Godfather (1972)", "Crime|Drama"),
        (18, "Pulp Fiction (1994)", "Crime|Drama|Thriller"),
        (19, "Fight Club (1999)", "Drama|Thriller"),
        (20, "Forrest Gump (1994)", "Drama|Romance|Comedy"),
        (21, "Schindler's List (1993)", "Drama|History"),
        (22, "The Silence of the Lambs (1991)", "Crime|Thriller|Drama"),
        (23, "Se7en (1995)", "Crime|Thriller|Drama"),
        (24, "Parasite (2019)", "Thriller|Drama|Comedy"),
        (25, "Whiplash (2014)", "Drama|Music"),
        (26, "The Social Network (2010)", "Drama"),
        (27, "Joker (2019)", "Crime|Drama|Thriller"),
        (28, "The Departed (2006)", "Crime|Drama|Thriller"),
        (29, "The Prestige (2006)", "Drama|Thriller|Mystery"),
        (30, "Shutter Island (2010)", "Mystery|Thriller|Drama"),
        
        # Animation & Family & Fantasy
        (31, "Spirited Away (2001)", "Animation|Fantasy|Adventure"),
        (32, "Toy Story (1995)", "Animation|Comedy|Family"),
        (33, "Toy Story 3 (2010)", "Animation|Comedy|Family"),
        (34, "Finding Nemo (2003)", "Animation|Comedy|Family"),
        (35, "The Lion King (1994)", "Animation|Drama|Musical"),
        (36, "WALL-E (2008)", "Animation|Sci-Fi|Family"),
        (37, "Up (2009)", "Animation|Comedy|Adventure"),
        (38, "Ratatouille (2007)", "Animation|Comedy|Family"),
        (39, "Princess Mononoke (1997)", "Animation|Fantasy|Adventure"),
        (40, "My Neighbor Totoro (1988)", "Animation|Fantasy|Family"),
        (41, "The Lord of the Rings: The Fellowship of the Ring (2001)", "Fantasy|Adventure|Action"),
        (42, "The Lord of the Rings: The Two Towers (2002)", "Fantasy|Adventure|Action"),
        (43, "The Lord of the Rings: The Return of the King (2003)", "Fantasy|Adventure|Action"),
        (44, "Harry Potter and the Sorcerer's Stone (2001)", "Fantasy|Adventure|Family"),
        (45, "Harry Potter and the Prisoner of Azkaban (2004)", "Fantasy|Adventure|Family"),
        
        # Comedy & Romance
        (46, "La La Land (201 LA)", "Romance|Musical|Drama"),
        (47, "Eternal Sunshine of the Spotless Mind (2004)", "Romance|Drama|Sci-Fi"),
        (48, "Amélie (2001)", "Romance|Comedy"),
        (49, "500 Days of Summer (2009)", "Romance|Comedy|Drama"),
        (50, "The Grand Budapest Hotel (2014)", "Comedy|Drama"),
        (51, "Superbad (2007)", "Comedy"),
        (52, "The Hangover (2009)", "Comedy"),
        (53, "Crazy Stupid Love (2011)", "Romance|Comedy|Drama"),
        (54, "Before Sunrise (1995)", "Romance|Drama"),
        (55, "Before Sunset (2004)", "Romance|Drama"),
        (56, "The Notebook (2004)", "Romance|Drama"),
        (57, "About Time (2013)", "Romance|Drama|Fantasy"),
        (58, "Mean Girls (2004)", "Comedy"),
        (59, "Step Brothers (2008)", "Comedy"),
        (60, "Scott Pilgrim vs. the World (2010)", "Comedy|Action|Fantasy")
    ]
    
    df_movies = pd.DataFrame(movies_data, columns=["movieId", "title", "genres"])
    return df_movies

def generate_ratings_dataset(df_movies, num_users=80, ratings_per_user=20, random_state=42):
    np.random.seed(random_state)
    
    # We will segment users into 4 archetypes (preferences) to create structural correlation
    # for collaborative filtering:
    # Group 1: Action & Sci-Fi lover (movies 1-15, 41-45)
    # Group 2: Drama & Thriller lover (movies 16-30)
    # Group 3: Animation & Fantasy lover (movies 31-45, 46-48)
    # Group 4: Comedy & Romance lover (movies 46-60, 20)
    
    ratings_list = []
    
    for user_id in range(1, num_users + 1):
        # Determine archetype
        archetype = (user_id % 4) + 1
        
        # Define favorite and least favorite movie IDs
        if archetype == 1:
            fav_movies = list(range(1, 16)) + list(range(41, 46))
            dislike_movies = list(range(46, 60))
        elif archetype == 2:
            fav_movies = list(range(16, 31))
            dislike_movies = list(range(31, 41)) + list(range(51, 60))
        elif archetype == 3:
            fav_movies = list(range(31, 46)) + [47, 48]
            dislike_movies = list(range(6, 14)) + list(range(17, 24))
        else: # archetype == 4
            fav_movies = list(range(46, 61)) + [20, 32, 33]
            dislike_movies = list(range(1, 14))
            
        # Select movies this user has rated
        all_movie_ids = df_movies["movieId"].tolist()
        
        # Assign probabilities of rating: highly likely to rate favorite/disliked movies
        p_rate = []
        for mid in all_movie_ids:
            if mid in fav_movies:
                p_rate.append(0.5)
            elif mid in dislike_movies:
                p_rate.append(0.3)
            else:
                p_rate.append(0.1)
                
        p_rate = np.array(p_rate)
        p_rate /= p_rate.sum()
        
        num_ratings = np.random.randint(15, ratings_per_user + 10)
        rated_movies = np.random.choice(all_movie_ids, size=min(num_ratings, len(all_movie_ids)), replace=False, p=p_rate)
        
        for mid in rated_movies:
            # Assign ratings based on archetype preference
            if mid in fav_movies:
                rating = np.random.choice([4.0, 4.5, 5.0], p=[0.2, 0.4, 0.4])
            elif mid in dislike_movies:
                rating = np.random.choice([1.0, 1.5, 2.0, 2.5], p=[0.3, 0.3, 0.2, 0.2])
            else:
                rating = np.random.choice([3.0, 3.5, 4.0], p=[0.4, 0.4, 0.2])
                
            ratings_list.append({
                "userId": user_id,
                "movieId": int(mid),
                "rating": float(rating),
                "timestamp": 1260759000 + np.random.randint(0, 1000000)
            })
            
    df_ratings = pd.DataFrame(ratings_list)
    return df_ratings

if __name__ == "__main__":
    os.makedirs("C:/Users/mvdev/Documents/movie-recommendation-system/data", exist_ok=True)
    
    print("Generating movies dataset...")
    df_movies = generate_movie_dataset()
    movies_path = "C:/Users/mvdev/Documents/movie-recommendation-system/data/movies.csv"
    df_movies.to_csv(movies_path, index=False)
    print(f"Saved {len(df_movies)} movies to {movies_path}")
    
    print("Generating user ratings dataset...")
    df_ratings = generate_ratings_dataset(df_movies)
    ratings_path = "C:/Users/mvdev/Documents/movie-recommendation-system/data/ratings.csv"
    df_ratings.to_csv(ratings_path, index=False)
    print(f"Saved {len(df_ratings)} ratings to {ratings_path}")
    print(f"Ratings distribution:")
    print(df_ratings["rating"].value_counts().sort_index())
