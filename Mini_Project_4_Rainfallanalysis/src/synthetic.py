"""SYNTHETIC multi-year rainfall (placeholder for real NASA POWER / UNMA data).

No network access was available when this was written, so year-to-year
noise is simulated around the illustrative monthly means, scaled by each
region's own CV. This is NOT real climate data: swap
`generate_synthetic_years()` for a NASA POWER / UNMA pull to get the real thing.
"""
import numpy as np

N_YEARS = 10


def generate_synthetic_years(region, n_years=N_YEARS, rng=None, seed=42):
    """Synthetic n_years x 12 rainfall matrix (mm).

    Gamma-distributed noise around each month's illustrative value, scaled by
    the region's CV (capped at 50% and damped by 0.6 so months rarely go
    negative-ish).
    """
    if rng is None:
        rng = np.random.default_rng(seed)
    cv = region.coefficient_of_variation() / 100.0
    years = np.zeros((n_years, 12))
    for m in range(12):
        mu = max(region.rainfall[m], 1.0)
        sigma = mu * min(cv, 0.5) * 0.6
        shape = (mu / sigma) ** 2
        scale = (sigma ** 2) / mu
        years[:, m] = rng.gamma(shape, scale, size=n_years)
    return years


def generate_all(regions, n_years=N_YEARS, seed=42):
    """One shared RNG across regions (reproducible, matches the original script)."""
    rng = np.random.default_rng(seed)
    return {name: generate_synthetic_years(r, n_years, rng=rng)
            for name, r in regions.items()}
