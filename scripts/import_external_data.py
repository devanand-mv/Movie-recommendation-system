import os
import io
import ssl
import urllib.request
import zipfile
import pandas as pd

# Official MovieLens Small Dataset URL (100,000 ratings, 9,700+ movies, 600 users)
MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

def download_and_import_movielens():
    data_dir = "C:/Users/mvdev/Documents/movie-recommendation-system/data"
    os.makedirs(data_dir, exist_ok=True)
    
    print("Downloading official MovieLens 100k dataset from GroupLens...")
    req = urllib.request.Request(
        MOVIELENS_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx) as response:
            zip_data = response.read()
        print("Download complete! Extracting dataset in memory...")
        
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            # List files in zip
            file_list = z.namelist()
            print(f"Extracted archive contents: {file_list}")
            
            # Read movies.csv and ratings.csv
            movies_file = [f for f in file_list if f.endswith("movies.csv")][0]
            ratings_file = [f for f in file_list if f.endswith("ratings.csv")][0]
            
            df_movies = pd.read_csv(z.open(movies_file))
            df_ratings = pd.read_csv(z.open(ratings_file))
            
            # Data cleaning: drop missing values, ensure types
            df_movies = df_movies.dropna(subset=["movieId", "title", "genres"])
            df_ratings = df_ratings.dropna(subset=["userId", "movieId", "rating"])
            
            # Filter out movies with (no genres listed) if any
            df_movies = df_movies[df_movies["genres"] != "(no genres listed)"]
            
            # Align ratings to only include valid movies in df_movies
            df_ratings = df_ratings[df_ratings["movieId"].isin(df_movies["movieId"])]
            
            # Output file paths
            output_movies_path = os.path.join(data_dir, "movies.csv")
            output_ratings_path = os.path.join(data_dir, "ratings.csv")
            
            # Save clean CSV files
            df_movies.to_csv(output_movies_path, index=False)
            df_ratings.to_csv(output_ratings_path, index=False)
            
            print("\n--- MovieLens Dataset Import Successful! ---")
            print(f"Movies Catalog: {len(df_movies):,} titles saved to {output_movies_path}")
            print(f"Ratings Matrix: {len(df_ratings):,} ratings saved to {output_ratings_path}")
            print(f"Unique Users: {df_ratings['userId'].nunique():,} active reviewers")
            print(f"Unique Genres: {len(set('|'.join(df_movies['genres']).split('|'))):,} distinct categories")
            print("\nSample Movies:")
            print(df_movies.head(5)[["movieId", "title", "genres"]].to_string(index=False))
            
    except Exception as e:
        print(f"Error downloading or parsing MovieLens dataset: {e}")

if __name__ == "__main__":
    download_and_import_movielens()
