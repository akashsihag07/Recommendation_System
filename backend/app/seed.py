import csv

from . import config
from .cleaning import clean_row
from .cleaning_indian import clean_indian_row
from .database import get_movies


def _load_csv(path, cleaner, encoding="utf-8"):
    docs = []
    with open(path, encoding=encoding) as f:
        for row in csv.DictReader(f):
            movie = cleaner(row)
            if movie is not None:
                docs.append(movie)
    return docs


def load_documents():
    hollywood = _load_csv(config.CSV_PATH, clean_row)
    indian = _load_csv(config.INDIA_CSV_PATH, clean_indian_row)
    print(f"[seed] cleaned {len(hollywood)} Hollywood + {len(indian)} Indian movies.")
    return hollywood + indian


def seed_if_empty():
    movies = get_movies()

    existing = movies.count_documents({})
    if existing > 0:
        print(f"[seed] {existing} movies already loaded, skipping.")
        return

    docs = load_documents()
    movies.insert_many(docs)

    movies.create_index("title")
    print(f"[seed] inserted {len(docs)} movies.")


if __name__ == "__main__":
    seed_if_empty()
