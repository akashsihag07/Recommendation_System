"""
Cleaning helpers for the second dataset: IMDb Movies India.

The goal is identical to cleaning.py - turn one messy CSV row into the *same*
movie dictionary shape - but this source is messy in different ways, so it needs
its own parsers:
    - Year looks like "(2019)"          -> 2019
    - Duration looks like "109 min"     -> 109
    - Genre is "Comedy, Drama" (plain text, not JSON) -> ["Comedy", "Drama"]
    - Votes look like "357,889"         -> 357889

It reuses the number helpers from cleaning.py so I'm not duplicating that logic.
This source has no overview or keywords, so those come out empty; it does have
cast + director, which I keep for the actor-preference feature later.
"""
import re

from .cleaning import to_int, to_float


def year_from_parens(raw: str):
    """'(2019)' -> 2019.  Pulls the first 4-digit number out, or None."""
    if not raw:
        return None
    match = re.search(r"\d{4}", raw)
    return int(match.group()) if match else None


def minutes_from_duration(raw: str):
    """'109 min' -> 109.  Grabs the leading number, defaults to 0."""
    if not raw:
        return 0
    match = re.search(r"\d+", raw)
    return int(match.group()) if match else 0


def split_genres(raw: str):
    """'Comedy, Drama' -> ['Comedy', 'Drama'].  Plain comma split, trimmed."""
    if not raw:
        return []
    return [g.strip() for g in raw.split(",") if g.strip()]


def votes_to_int(raw: str):
    """'357,889' -> 357889.  Strips the thousands commas first."""
    if not raw:
        return 0
    return to_int(raw.replace(",", ""))


def clean_indian_row(row: dict):
    """
    Turn one IMDb-India CSV row into the same movie document shape as
    cleaning.clean_row(), or None if it's missing the essentials.

    This source often has blank ratings, so - unlike the TMDB cleaner - a
    missing rating is also a reason to drop the row, since the rating drives both
    the rating filter and part of the score.
    """
    title = (row.get("Name") or "").strip()
    genres = split_genres(row.get("Genre", ""))
    rating = row.get("Rating")

    if not title or not genres or not rating:
        return None

    # keep the named cast members that actually exist (for the actor feature)
    cast = [
        row.get(col, "").strip()
        for col in ("Actor 1", "Actor 2", "Actor 3")
        if (row.get(col) or "").strip()
    ]

    return {
        "tmdb_id": 0,                       # this source has no TMDB id
        "title": title,
        "year": year_from_parens(row.get("Year", "")),
        "rating": to_float(rating),
        "vote_count": votes_to_int(row.get("Votes", "")),
        "popularity": 0.0,                  # no popularity field in this source
        "runtime": minutes_from_duration(row.get("Duration", "")),
        "language": "hi",                   # approx - dataset doesn't say, mostly Hindi
        "overview": "",                     # not provided by this source
        "genres": genres,
        "keywords": [],                     # not provided by this source
        "source": "indian",
        "cast": cast,
        "director": (row.get("Director") or "").strip(),
    }
