import json


def parse_names(raw: str):
    if not raw:
        return []
    try:
        items = json.loads(raw)
        return [it["name"] for it in items if it.get("name")]
    except (json.JSONDecodeError, TypeError):
        return []


def to_int(value, default=0):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def to_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def year_from_date(date_str: str):
    if date_str and len(date_str) >= 4:
        return to_int(date_str[:4], default=None)
    return None


def clean_row(row: dict):
    title = (row.get("title") or "").strip()
    genres = parse_names(row.get("genres", ""))

    
    if not title or not genres:
        return None

    return {
        "tmdb_id": to_int(row.get("id")),
        "title": title,
        "year": year_from_date(row.get("release_date", "")),
        "rating": to_float(row.get("vote_average")),
        "vote_count": to_int(row.get("vote_count")),
        "popularity": to_float(row.get("popularity")),
        "runtime": to_int(row.get("runtime")),
        "language": (row.get("original_language") or "en").strip(),
        "overview": (row.get("overview") or "").strip(),
        "genres": genres,
        "keywords": parse_names(row.get("keywords", "")),
        "source": "hollywood",
    }
