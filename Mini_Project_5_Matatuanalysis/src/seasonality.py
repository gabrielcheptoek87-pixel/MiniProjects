"""Extension: weekly-seasonality simulation and Seasonal-Naive vs Moving Average backtest."""
import numpy as np

from .forecasters import MovingAverageForecaster, SeasonalNaiveForecaster

# Day 0 = Monday ... Day 6 = Sunday
WEEKDAY_EFFECT = {0: 0, 1: 2, 2: 3, 3: 5, 4: 15, 5: 8, 6: -15}


def simulate_counts(n_days=60, base=50, noise_sd=3.0, seed=42, effects=WEEKDAY_EFFECT):
    rng = np.random.default_rng(seed)
    weekday = np.arange(n_days) % 7
    seasonal = np.array([effects[d] for d in weekday])
    counts = base + seasonal + rng.normal(0, noise_sd, n_days)
    return np.clip(counts, 5, None)


def backtest_seasonal(counts, period=7, ma_window=3):
    """Backtest from index `period` onward. Returns (ma_mae, sn_mae, ma_errors, sn_errors)."""
    ma_err, sn_err = [], []
    for t in range(period, len(counts)):
        hist, actual = counts[:t], counts[t]
        ma_err.append(abs(MovingAverageForecaster(ma_window).fit(hist).forecast_next() - actual))
        sn_err.append(abs(SeasonalNaiveForecaster(period).fit(hist).forecast_next() - actual))
    return float(np.mean(ma_err)), float(np.mean(sn_err)), ma_err, sn_err
