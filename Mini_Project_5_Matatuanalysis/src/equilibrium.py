"""Supply-demand equilibrium via a linear system.

Qd = 120 - 0.02P  ->  Q + 0.02P = 120
Qs =  10 + 0.03P  ->  Q - 0.03P = 10
"""
import numpy as np
from scipy.linalg import solve


def solve_equilibrium(d_intercept=120.0, d_slope=0.02, s_intercept=10.0, s_slope=0.03):
    """Return (Q*, P*) for Qd = a - b*P and Qs = c + d*P."""
    A = np.array([[1.0, d_slope], [1.0, -s_slope]])
    b = np.array([d_intercept, s_intercept])
    q, p = solve(A, b)
    return float(q), float(p)


def interpret_fare(current_fare: float, p_eq: float) -> str:
    """Plain-language reading of current fare vs equilibrium fare."""
    gap = abs(p_eq - current_fare)
    if current_fare < p_eq:
        return (f"Current fare (UGX {current_fare:,.0f}) is BELOW equilibrium by UGX {gap:,.2f}: "
                "demand exceeds supply (overcrowding/queuing). Raise the fare toward "
                "equilibrium or add vehicles.")
    return (f"Current fare (UGX {current_fare:,.0f}) is ABOVE equilibrium by UGX {gap:,.2f}: "
            "supply exceeds demand (under-full vehicles). Lowering the fare would raise ridership.")
