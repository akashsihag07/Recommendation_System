"""

Pydantic models used by the API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class UserPrefs(BaseModel):
    """Search preferences from the client."""

    genres: List[str] = Field(default_factory=list)
    min_rating: float = 0.0
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    fav_movie: Optional[str] = None
    lang: str = "any"
    limit: int = 12


class MovieRes(BaseModel):
    """Movie details returned by the API."""

    title: str
    year: Optional[int] = None
    rating: float
    genres: List[str]
    desc: str
    runtime: int
    lang: str
    score: float
    reason: str