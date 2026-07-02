import re

from .cleaning import to_int, to_float


def year_from_parens(raw: str):
    if not raw:
        return None
    match = re.search(r"\d{4}", raw)
    return int(match.group()) if match else None


def minutes_from_duration(raw: str):
    if not raw:
        return 0
    match = re.search(r"\d+", raw)
    return int(match.group()) if match else 0


def split_genres(raw: str):
    if not raw:
        return []
    return [g.strip() for g in raw.split(",") if g.strip()]


def votes_to_int(raw: str):
    if not raw:
        return 0
    return to_int(raw.replace(",", ""))


def clean_indian_row(row: dict):
    title = (row.get("Name") or "").strip()
    genres = split_genres(row.get("Genre", ""))
    rating = row.get("Rating")

    if not title or not genres or not rating:
        return None

    cast = [
        row.get(col, "").strip()
        for col in ("Actor 1", "Actor 2", "Actor 3")
        if (row.get(col) or "").strip()
    ]

    return {
        "tmdb_id": 0,                       
        "title": title,
        "year": year_from_parens(row.get("Year", "")),
        "rating": to_float(rating),
        "vote_count": votes_to_int(row.get("Votes", "")),
        "popularity": 0.0,                  
        "runtime": minutes_from_duration(row.get("Duration", "")),
        "language": "hi",                  
        "overview": "",                     
        "genres": genres,
        "keywords": [],                     
        "source": "indian",
        "cast": cast,
        "director": (row.get("Director") or "").strip(),
    }
