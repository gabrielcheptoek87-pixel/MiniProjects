"""Pairwise similarity / distance between regional rainfall vectors."""
import numpy as np
from scipy.spatial.distance import cosine as scipy_cosine

from .data import REGIONS


def cosine_similarity(a, b):
    """(a . b) / (||a|| * ||b||).

    Fixes last year's version, which used math.cos() -- that takes a single
    angle in radians and has nothing to do with comparing two vectors.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def verify_cosine_against_scipy(regions=None):
    """Check similarity == 1 - scipy cosine distance for every region pair.

    Returns a list of dicts (one per pair).
    """
    regions = regions or REGIONS
    names = list(regions)
    out = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = regions[names[i]].rainfall, regions[names[j]].rainfall
            sim = cosine_similarity(a, b)
            dist = scipy_cosine(a, b)
            out.append({
                "Pair": f"{names[i]} vs {names[j]}",
                "cosine_similarity": round(sim, 6),
                "scipy_distance": round(float(dist), 6),
                "1 - scipy_distance": round(1 - float(dist), 6),
                "match": bool(np.isclose(sim, 1 - dist, atol=1e-9)),
            })
    return out


def build_matrices(regions=None):
    """Return (names, cosine, pearson, euclidean) matrices."""
    regions = regions or REGIONS
    names = list(regions)
    n = len(names)
    cos_mat = np.zeros((n, n))
    pearson_mat = np.zeros((n, n))
    eucl_mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = regions[names[i]].rainfall, regions[names[j]].rainfall
            cos_mat[i, j] = cosine_similarity(a, b)
            pearson_mat[i, j] = np.corrcoef(a, b)[0, 1]
            eucl_mat[i, j] = np.linalg.norm(a - b)
    return names, cos_mat, pearson_mat, eucl_mat
