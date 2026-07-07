"""

Recommendation logic and ranking.
"""

import math
import re

from . import config, scoring
from .database import get_movies_coll


def build_query(prefs):
    """Build the MongoDB query."""
    query = {"votes": {"$gte": config.MIN_VOTES}}
    if prefs.min_rating:
        query["rating"] = {"$gte": prefs.min_rating}
    year_filter = {}
    if prefs.year_from:
        year_filter["$gte"] = prefs.year_from
    if prefs.year_to:
        year_filter["$lte"] = prefs.year_to
    if year_filter:
        query["year"] = year_filter
    if prefs.lang and prefs.lang != "any":
        query["lang"] = prefs.lang
    return query


def find_fav(title):
    """Find the selected favorite movie."""
    if not title:
        return None
    pattern = "^" + re.escape(title.strip()) + "$"
    return get_movies_coll().find_one(
        {"title": {"$regex": pattern, "$options": "i"}}
    )


def get_recs(prefs):
    """Generate movie recommendations."""
    coll = get_movies_coll()
    user_genres = {g.strip() for g in prefs.genres if g.strip()}
    candidates = list(coll.find(build_query(prefs)))
    fav = find_fav(prefs.fav_movie)
    fav_genres = set(fav["genres"]) if fav else set()
    fav_tags = set(fav.get("tags", [])) if fav else set()
    max_pop = max((m.get("pop", 0) for m in candidates), default=1.0) or 1.0
    max_log = math.log1p(max_pop)
    results = []
    for movie in candidates:
        if fav and movie["_id"] == fav["_id"]:
            continue
        movie_genres = set(movie.get("genres", []))
        genre_score = scoring.score_genres(user_genres, movie_genres)
        similarity = (
            scoring.score_tags(
                fav_genres,
                fav_tags,
                movie_genres,
                set(movie.get("tags", [])),
            )
            if fav
            else 0.0
        )
        pop_score = scoring.score_pop(movie.get("pop", 0), max_log)
        total = scoring.calc_total(
            genre_score,
            similarity,
            movie.get("rating", 0),
            pop_score,
        )
        if user_genres and genre_score == 0 and not fav:
            continue
        results.append((total, movie))
    results.sort(key=lambda item: item[0], reverse=True)
    return [
        format_res(score, user_genres, movie)
        for score, movie in results[: prefs.limit]
    ]


def format_res(score, picked, movie):
    """Format a movie for the API."""
    movie_genres = set(movie.get("genres", []))
    return {
        "title": movie.get("title", ""),
        "year": movie.get("year"),
        "rating": round(movie.get("rating", 0), 1),
        "genres": movie.get("genres", []),
        "desc": movie.get("desc", ""),
        "runtime": movie.get("runtime", 0),
        "lang": movie.get("lang", ""),
        "score": round(score * 100, 1),
        "reason": get_reason(picked, movie_genres, movie),
        "poster": movie.get("poster", ""), #updating for poster and votes
        "votes": movie.get("votes", 0),
    }


def get_reason(picked, movie_genres, movie):
    """Create a short match summary."""
    parts = []
    if picked:
        shared = picked & movie_genres
        if shared:
            parts.append(f"Matches {len(shared)}/{len(picked)} genres")
    if movie.get("rating"):
        parts.append(f"{round(movie['rating'], 1)}★")
    if not parts:
        parts.append("Popular pick")
    return " · ".join(parts)
