"""recommend.py

Recommendation endpoints.
"""

from typing import List

from fastapi import APIRouter, HTTPException

from .. import recommender
from ..schemas import MovieRes, UserPrefs

router = APIRouter()


@router.post("/recommend", response_model=List[MovieRes])
def get_recommendations(prefs: UserPrefs):
    """Return movie recommendations."""
    if not 1 <= prefs.limit <= 50:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 50",
        )

    return recommender.get_recs(prefs)