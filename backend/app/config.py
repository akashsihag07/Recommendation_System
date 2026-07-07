import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017")
DB_NAME = os.getenv("DB_NAME", "moviedb")
MOVIES_COLLECTION = os.getenv("MOVIES_COLLECTION", "movies")

# the movie dataset inside the container (copied in by the Dockerfile)
CSV_PATH = os.getenv("CSV_PATH", "/app/data/tmdb_movies_clean.csv")

# movies with very few votes have unreliable ratings, so we ignore them
MIN_VOTES = int(os.getenv("MIN_VOTES", "25"))

VECTORS_PATH = os.getenv("VECTORS_PATH", "/app/data/overview_vectors.npz")