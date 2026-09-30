"""Descriptive statistics, cost model, Monte Carlo sensitivity."""
from __future__ import annotations

import statistics as stats_mod

import numpy as np

from .config import BATTERY_COST_UGX, RNG_SEED, SOLAR_COST_UGX


def usage_stats(X):
    def s(arr):
        return {
            "mean": stats_mod.mean(arr),
            "variance": stats_mod.variance(arr),
            "stdev": stats_mod.stdev(arr),
        }
    return {"solar": s(list(X[0])), "battery": s(list(X[1]))}


def cost_model(X):
    daily_cost = X[0] * SOLAR_COST_UGX + X[1] * BATTERY_COST_UGX
    return daily_cost, float(daily_cost.sum())


def sensitivity_analysis(grid, d1, d2, pct=0.05, n_draws=1000, seed=RNG_SEED):
    """Perturb D1, D2 uniformly by +-pct and re-solve. Returns (X, x_base, y_base)."""
    rng = np.random.default_rng(seed)
    D1p = d1 + rng.uniform(-pct, pct, n_draws) * d1
    D2p = d2 + rng.uniform(-pct, pct, n_draws) * d2
    X = grid.solve_batch_vectorised(np.vstack([D1p, D2p]))
    x_base, y_base = grid.solve_day(d1, d2)
    return X, x_base, y_base
