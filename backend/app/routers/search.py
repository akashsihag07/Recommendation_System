"""search.py

Search endpoints.
"""

import re

from fastapi import APIRouter

from ..database import get_movies_coll

router = APIRouter()


@router.get("/movies/search")
def search_titles(q: str = ""):
    """Search movie titles."""
    query = q.strip()

    if len(query) < 2:
        return {"results": []}

    coll = get_movies_coll()

    matches = (
        coll.find(
            {"title": {"$regex": re.escape(query), "$options": "i"}},
            {"_id": 0, "title": 1},
        )
        .sort("pop", -1)
        .limit(8)
    )

    return {"results": [movie["title"] for movie in matches]}