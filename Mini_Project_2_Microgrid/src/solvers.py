"""Batch-solve timing and infeasibility handling."""
from __future__ import annotations

import timeit

import numpy as np
import pandas as pd
from scipy.optimize import nnls


def time_solvers(grid, D, number=300):
    """Return (avg_loop_seconds, avg_vectorised_seconds) per call."""
    t_loop = timeit.timeit(lambda: grid.solve_batch_loop(D), number=number) / number
    t_vec = timeit.timeit(lambda: grid.solve_batch_vectorised(D), number=number) / number
    return t_loop, t_vec


def handle_infeasible(grid, X, D):
    """
    Flag days where the raw solution has a negative x or y (not physically
    realisable). Re-solve flagged days with non-negative least squares, which
    finds the closest dispatch satisfying x, y >= 0.

    Returns (X_clean, report_dataframe).
    """
    n = X.shape[1]
    flagged = np.any(X < 0, axis=0)
    X_clean = X.copy()
    for i in np.where(flagged)[0]:
        sol, _ = nnls(grid.A, D[:, i])
        X_clean[:, i] = sol

    report = pd.DataFrame({
        "day": np.arange(1, n + 1),
        "x_raw": X[0],
        "y_raw": X[1],
        "infeasible": flagged,
        "x_fixed": X_clean[0],
        "y_fixed": X_clean[1],
    })
    return X_clean, report
