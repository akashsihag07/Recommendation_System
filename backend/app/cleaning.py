"""
Helpers for cleaning movie data.

Turns one raw CSV row into the shape stored in Mongo. Everything here
runs at seed time, once, so it can be defensive without costing anything.
"""


def safe_int(val, default=0):
    """
    Int or default. CSV fields come through as strings and some are junk.

    Goes via float first so "7.0" doesn't blow up.
    """
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def safe_float(val, default=0.0):
    """Float or default, for the same reason as safe_int."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def parse_tags(txt):
    """
    Comma separated string to a list. Genres and keywords arrive this way.

    Strips whitespace and drops empties, so trailing commas are harmless.
    """
    if not txt:
        return []

    return [tag.strip() for tag in txt.split(",") if tag.strip()]


def get_year(date_str):
    """
    Year out of a release date. Returns None if the date is missing or short.

    Just takes the first four chars rather than parsing the whole date,
    since the year is all we filter on.
    """
    if date_str and len(date_str) >= 4:
        return safe_int(date_str[:4], default=None)

    return None


def parse_row(row):
    """
    One CSV row to one movie doc, or None if it isn't usable.

    Title, genres and overview are required. Without them the movie can't
    be matched or shown, so it's dropped rather than stored half empty.
    Keys are shortened here, so the rest of the app reads desc and pop
    rather than overview and popularity.
    """
    title = (row.get("title") or "").strip()
    genres = parse_tags(row.get("genres", ""))
    desc = (row.get("overview") or "").strip()

    if not title or not genres or not desc:
        return None

    return {
        "tmdb_id": safe_int(row.get("id")),
        "title": title,
        "year": get_year(row.get("release_date", "")),
        "rating": safe_float(row.get("vote_average")),
        "votes": safe_int(row.get("vote_count")),
        "pop": safe_float(row.get("popularity")),
        "runtime": safe_int(row.get("runtime")),
        "lang": (row.get("original_language") or "").strip(),
        "desc": desc,
        "genres": genres,
        "tags": parse_tags(row.get("keywords", "")),
        "poster": (row.get("poster_path") or "").strip(),# i have added new column for poster image..
    }