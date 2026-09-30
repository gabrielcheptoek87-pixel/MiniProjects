"""Bootstrap prediction intervals from model residuals."""

import numpy as np


def bootstrap_interval(model, horizon, rng, n_boot=1000, level=95):
    """Resample in-sample residuals to build a prediction interval.

    `rng` is a numpy RandomState/Generator, so callers control reproducibility.
    Returns (lower, upper) arrays of length `horizon`.
    """
    residuals = model.values_ - model.fitted_values()
    base = model.predict(horizon)
    boot = np.zeros((n_boot, horizon))
    for b in range(n_boot):
        boot[b] = base + rng.choice(residuals, size=horizon, replace=True)
    tail = (100 - level) / 2
    return np.percentile(boot, tail, axis=0), np.percentile(boot, 100 - tail, axis=0)


def bootstrap_all(districts, models, horizon, rng, n_boot=1000):
    return {name: bootstrap_interval(models[name], horizon, rng, n_boot)
            for name in districts}
