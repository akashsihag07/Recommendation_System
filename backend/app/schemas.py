"""

Pydantic models used by the API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

class ScoringWeights(BaseModel):
    """Optional scoring weights the four scoring components. sum should = to 1."""
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
    limit: int = 12
    weights: Optional[ScoringWeights] = None #for scoring weights


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
    #i am updating for poster,votes
    poster: str
<<<<<<< Updated upstream
    votes:  int
=======
    votes:  int
>>>>>>> Stashed changes
