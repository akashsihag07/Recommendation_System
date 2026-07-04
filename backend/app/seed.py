"""Seed the database with the movie dataset."""

import csv

from . import config
from .cleaning import parse_row
from .database import get_movies_coll


def load_data():
    """Load and clean movie data."""
    movies = []
    with open(config.CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie = parse_row(row)
            if movie:
                movies.append(movie)
    return movies


def init_db():
    """Seed the collection if needed."""
    coll = get_movies_coll()
    if coll.count_documents({}):
        print("[seed] data already exists, skipping.")
        return
    movies = load_data()
    coll.insert_many(movies)
    # Used by the search/filter endpoints.
    coll.create_index("title")
    coll.create_index("lang")
    print(f"[seed] inserted {len(movies)} movies.")


if __name__ == "__main__":
    init_db()