"""Core linear models: 2x2 solar/battery grid and 3x3 hybrid with diesel.

    3x + 2y = D1     (daytime load, kWh)
    4x +  y = D2     (critical-equipment load, kWh)
"""
from __future__ import annotations

import numpy as np
import scipy.linalg



class MicroGrid:
    """2x2 linear model of a solar + battery micro-grid."""

    def __init__(self):
        # Coefficient matrix for unknowns [x (solar), y (battery)]
        self.A = np.array([[3.0, 2.0],
                           [4.0, 1.0]])
        self.labels = ["solar (x)", "battery (y)"]

    def diagnostics(self, verbose=True):
        """Compute determinant + condition number and explain what they mean."""
        det = np.linalg.det(self.A)
        cond = np.linalg.cond(self.A)
        if verbose:
            print(f"[{self.__class__.__name__}] determinant = {det:.4f}, "
                  f"condition number = {cond:.4f}")
            if abs(det) < 1e-8:
                print("  -> SINGULAR: the equations do not pin down a unique "
                      "dispatch. Either no solution exists, or infinitely "
                      "many do (one equation is a multiple/combination of "
                      "the other(s)).")
            elif cond > 50:
                print("  -> POORLY CONDITIONED: the matrix is close to "
                      "singular. Small measurement noise or rounding in "
                      "D1/D2 will be amplified into much larger errors in "
                      "the solved x, y.")
            else:
                print("  -> WELL-CONDITIONED: the system is numerically "
                      "stable. A small relative change in demand produces "
                      "a proportionally small change in the dispatch.")
        return det, cond

    def solve_day(self, d1, d2):
        """Solve for (x, y) given one day's demand figures."""
        det, _ = self.diagnostics(verbose=False)
        if abs(det) < 1e-10:
            raise np.linalg.LinAlgError(
                "Coefficient matrix is singular for this configuration; "
                "cannot solve for a unique dispatch.")
        b = np.array([d1, d2], dtype=float)
        return scipy.linalg.solve(self.A, b)

    def solve_batch_loop(self, D):
        """D: (k, n) array of stacked RHS vectors. Solve one column at a time."""
        n = D.shape[1]
        out = np.empty_like(D, dtype=float)
        for i in range(n):
            out[:, i] = scipy.linalg.solve(self.A, D[:, i])
        return out

    def solve_batch_vectorised(self, D):
        """D: (k, n) array. scipy.linalg.solve accepts a 2-D RHS directly,
        factorising A once and solving for every column in one call."""
        return scipy.linalg.solve(self.A, D)


class HybridMicroGrid(MicroGrid):
    """
    Extension: adds a diesel generator z.

        3x + 2y + 0z = D1   (daytime load - diesel not used by day)
        4x +  y +  z = D2   (critical load - diesel can back up)
         x +  y +  z = D3   (total energy dispatched must meet total demand)

    Pass singular_demo=True to replace the third row with a combination of
    the first two, producing a linearly-dependent (singular) system.
    """

    def __init__(self, singular_demo=False):
        self.A = np.array([[3.0, 2.0, 0.0],
                           [4.0, 1.0, 1.0],
                           [1.0, 1.0, 1.0]])
        if singular_demo:
            # row3 := row1 - row2  -> linearly dependent on rows 1 & 2
            self.A[2] = self.A[0] - self.A[1]
        self.labels = ["solar (x)", "battery (y)", "diesel (z)"]

    def solve_day(self, d1, d2, d3):
        det, _ = self.diagnostics(verbose=False)
        if abs(det) < 1e-10:
            raise np.linalg.LinAlgError(
                "3x3 system is singular: the third equation is linearly "
                "dependent on the first two, so there is no unique "
                "(x, y, z) -- either no solution, or a whole line/plane "
                "of equally valid solutions.")
        b = np.array([d1, d2, d3], dtype=float)
        return scipy.linalg.solve(self.A, b)
