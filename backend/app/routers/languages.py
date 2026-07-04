"""languages.py

Language endpoints.
"""

from fastapi import APIRouter

from ..database import get_movies_coll

router = APIRouter()


@router.get("/languages")
def get_top_languages():
    """Return available languages."""
    coll = get_movies_coll()

    pipeline = [
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    languages = coll.aggregate(pipeline)

    return {
        "languages": [
            {"code": lang["_id"], "count": lang["count"]}
            for lang in languages
            if lang["_id"]
        ]
    }