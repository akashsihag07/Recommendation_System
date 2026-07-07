"""Loads precomputed overview vectors and computes cosine similarity."""

import numpy as np

from . import config

_index = {}
_vecs = None


def load_vectors():
    global _index, _vecs
    try:
        data = np.load(config.VECTORS_PATH)
        _vecs = data["vectors"].astype(np.float32)
        _index = {int(i): n for n, i in enumerate(data["ids"])}
        print(f"[vectors] loaded {len(_index)} overview vectors.")
    except FileNotFoundError:
        print("[vectors] vector file missing, semantic similarity disabled.")


def get_vec(tmdb_id):
    n = _index.get(int(tmdb_id)) if tmdb_id is not None else None
    return _vecs[n] if n is not None else None


def cosine(v1, v2):
    return float(np.dot(v1, v2))