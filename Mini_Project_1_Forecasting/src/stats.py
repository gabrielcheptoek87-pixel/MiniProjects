"""Descriptive statistics and growth rates."""

import statistics

import numpy as np


def descriptive_stats(district):
    """Return (statistics-module dict, NumPy dict) for one district."""
    vals = district.populations
    vals_list = vals.tolist()
    stats_mod = {
        "mean": statistics.mean(vals_list),
        "median": statistics.median(vals_list),
        "variance": statistics.variance(vals_list),   # sample, ddof=1
        "stdev": statistics.stdev(vals_list),         # sample, ddof=1
    }
    numpy_mod = {
        "mean": np.mean(vals),
        "median": np.median(vals),
        "variance_pop": np.var(vals, ddof=0),
        "variance_sample": np.var(vals, ddof=1),
        "std_pop": np.std(vals, ddof=0),
        "std_sample": np.std(vals, ddof=1),
    }
    return stats_mod, numpy_mod


def yoy_growth(pops):
    """Year-on-year growth in percent."""
    return (pops[1:] - pops[:-1]) / pops[:-1] * 100


def cagr(pops):
    """Compound annual growth rate (fraction) over the whole series."""
    return (pops[-1] / pops[0]) ** (1 / (len(pops) - 1)) - 1
