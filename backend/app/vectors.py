"""Loads precomputed overview vectors and computes cosine similarity.
Vectors are generated offline in Kaggle. vecs is the matrix._index maps a tmdb id to its row"""

import numpy as np

from . import config

_index = {}
_vecs = None


def load_vectors():
    """
Read the npz file into memory. Called once at startup from main.
Stored as float16 to halve the file size, upcast to float32 here because
it is faster on CPU. A missing file is not fatal, callers fall back to
Jaccard only.
"""
    global _index, _vecs
    try:
        data = np.load(config.VECTORS_PATH)
        _vecs = data["vectors"].astype(np.float32)
        _index = {int(i): n for n, i in enumerate(data["ids"])}
        print(f"[vectors] loaded {len(_index)} overview vectors.")
    except FileNotFoundError:
        print("[vectors] vector file missing, semantic similarity disabled.")


def get_vec(tmdb_id):
    """
Return the vector for a tmdb id, or None if there isn't one.
Uses get rather than direct indexing because 28 movies have no vector.
"""
    n = _index.get(int(tmdb_id)) if tmdb_id is not None else None
    return _vecs[n] if n is not None else None


def cosine(v1, v2):
    """
Cosine similarity between two vectors.
Just a dot product, since the vectors were normalized when they were
generated. Both magnitudes are 1, so the division drops out.
"""
    return float(np.dot(v1, v2))