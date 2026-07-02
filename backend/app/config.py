import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017")


DB_NAME = os.getenv("DB_NAME", "moviedb")
MOVIES_COLLECTION = os.getenv("MOVIES_COLLECTION", "movies")


CSV_PATH = os.getenv("CSV_PATH", "/app/data/tmdb_5000_movies.csv")
INDIA_CSV_PATH = os.getenv("INDIA_CSV_PATH", "/app/data/imdb_india.csv")

MIN_VOTES = int(os.getenv("MIN_VOTES", "50"))
