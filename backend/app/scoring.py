"""
Scoring helpers for movie recommendations.This module contains helper functions for computing genre, tag,
popularity, and rating scores. All functions are stateless and
return normalized values that can be combined into the final
recommendation score.
"""

import math


# Weights for the final score.
W = {
    "gen": 0.50,
    "sim": 0.25,
    "rat": 0.15,
    "pop": 0.10,
}


def get_jaccard(s1, s2):
    """Compute Jaccard similarity between two sets of tags or genres."""
    if not s1 or not s2:
        return 0.0

    common = len(s1 & s2)
    total = len(s1 | s2)

    return common / total


def score_genres(user_gens, movie_gens):
    """Calculate how well a movie matches the user's selected genres."""
    if not user_gens:
        return 0.0

    matches = len(user_gens & movie_gens)
    return matches / len(user_gens)


def score_tags(fav_g, fav_k, mov_g, mov_k):
    """Compute tag similarity between the fav movie and a candidate movie."""
    genre_score = get_jaccard(fav_g, mov_g)
    tag_score = get_jaccard(fav_k, mov_k)

    return 0.6 * genre_score + 0.4 * tag_score


def score_pop(pop_val, max_log):
    """Normalize popularity into score between 0 and 1 ."""
    if max_log <= 0:
        return 0.0

    return math.log1p(pop_val) / max_log

#writing w for scoring weights, return main small w and if condition
def calc_total(g_score, sim_score, rating, pop_score,w=None):
    """Combine all scoring components into the final recommendation score."""
    if w is None:
        w = W
    rating_score = rating / 10.0

    return (
        w["gen"] * g_score
        + w["sim"] * sim_score
        + w["rat"] * rating_score
        + w["pop"] * pop_score
    )

def blend_sim(semantic, tag):
    """Blend semantic and tag similarity into a single similarity score.
    """
    return 0.7 * semantic + 0.3 * tag