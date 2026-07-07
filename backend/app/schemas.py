"""schemas.py

Pydantic models used by the API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    """Optional scoring weights. Should sum to 1."""

    gen: float = 0.50
    sim: float = 0.25
    rat: float = 0.15
    pop: float = 0.10


class UserPrefs(BaseModel):
    """Search preferences from the client."""

    genres: List[str] = Field(default_factory=list)
    min_rating: float = 0.0
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    fav_movie: Optional[str] = None
    lang: str = "any"
    weights: Optional[ScoringWeights] = None
    limit: int = 12


class MovieRes(BaseModel):
    """Movie details returned by the API."""

    title: str
    year: Optional[int] = None
    rating: float
    votes: int
    genres: List[str]
    desc: str
    runtime: int
    lang: str
    poster: str
    score: float
    reason: str