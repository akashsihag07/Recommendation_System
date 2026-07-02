
from pymongo import MongoClient

from . import config


_client = MongoClient(config.MONGO_URI)
_db = _client[config.DB_NAME]


def get_movies():
    return _db[config.MOVIES_COLLECTION]


def ping():
    _client.admin.command("ping")
