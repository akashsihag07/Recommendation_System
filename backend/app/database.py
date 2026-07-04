"""

MongoDB connection helpers.
"""

from pymongo import MongoClient

from . import config

_client = MongoClient(config.MONGO_URI)
_db = _client[config.DB_NAME]


def get_movies_coll():
    """Return the movies collection."""
    return _db[config.MOVIES_COLLECTION]


def check_db():
    """Check the database connection."""
    _client.admin.command("ping")