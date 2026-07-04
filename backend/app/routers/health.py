"""health.py

Health check endpoint.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def ping():
    """Return the API status."""
    return {
        "status": "ok",
        "service": "Movie Matcher API",
    }