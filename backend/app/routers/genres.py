"""genres.py

Genre endpoints.
"""

from fastapi import APIRouter

from ..database import get_movies_coll

router = APIRouter()


@router.get("/genres")
def get_all_genres():
    """Return the available genres."""
    coll = get_movies_coll()

    genres = sorted(g for g in coll.distinct("genres") if g)

    return {"genres": genres}