"""Rolling-origin backtesting, alpha grid search, model selection, day-ahead forecast."""
import numpy as np

from .forecasters import (
    ExponentialSmoothingForecaster,
    LinearTrendForecaster,
    MovingAverageForecaster,
)


def rolling_origin_mae(factory, counts, test_days) -> float:
    """MAE over 1-indexed `test_days`; each day is forecast from days before it."""
    counts = np.asarray(counts, dtype=float)
    errors = []
    for day in test_days:
        pred = factory().fit(counts[: day - 1]).forecast_next()
        errors.append(abs(pred - counts[day - 1]))
    return float(np.mean(errors))


def grid_search_alpha(counts, test_days, alphas=None):
    """Return (best_alpha, {alpha: mae})."""
    if alphas is None:
        alphas = [round(a, 1) for a in np.arange(0.1, 1.0, 0.1)]
    maes = {a: rolling_origin_mae(lambda a=a: ExponentialSmoothingForecaster(a), counts, test_days)
            for a in alphas}
    return min(maes, key=maes.get), maes


def build_candidates(best_alpha: float) -> dict:
    """Model name -> factory."""
    return {
        "MovingAverage(3)": lambda: MovingAverageForecaster(3),
        f"SES(alpha={best_alpha})": lambda: ExponentialSmoothingForecaster(best_alpha),
        "LinearTrend": lambda: LinearTrendForecaster(),
    }


def evaluate_route(counts, test_days):
    """Run the full model comparison for one route.

    Returns dict: best_alpha, alpha_maes, maes, best_model, forecast (next-day passengers).
    """
    best_alpha, alpha_maes = grid_search_alpha(counts, test_days)
    candidates = build_candidates(best_alpha)
    maes = {n: rolling_origin_mae(f, counts, test_days) for n, f in candidates.items()}
    best_model = min(maes, key=maes.get)
    forecast = candidates[best_model]().fit(counts).forecast_next()
    return {"best_alpha": best_alpha, "alpha_maes": alpha_maes, "maes": maes,
            "best_model": best_model, "forecast": forecast}
