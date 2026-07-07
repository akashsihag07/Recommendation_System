"""

Helpers for cleaning movie data.
"""


def safe_int(val, default=0):
    """Convert to int."""
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def safe_float(val, default=0.0):
    """Convert to float."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def parse_tags(txt):
    """Split a comma-separated string."""
    if not txt:
        return []

    return [tag.strip() for tag in txt.split(",") if tag.strip()]


def get_year(date_str):
    """Extract the release year."""
    if date_str and len(date_str) >= 4:
        return safe_int(date_str[:4], default=None)

    return None


def parse_row(row):
    """Clean a CSV row."""
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
