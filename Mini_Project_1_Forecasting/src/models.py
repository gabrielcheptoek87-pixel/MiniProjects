"""Forecasting models sharing a common abstract interface."""

from abc import ABC, abstractmethod

import numpy as np


class Forecaster(ABC):
    """Abstract base class for a population forecasting model."""

    def __init__(self):
        self.years_ = None
        self.values_ = None
        self.fitted_ = None

    @abstractmethod
    def fit(self, years, values):
        ...

    @abstractmethod
    def predict(self, horizon):
        """Return `horizon` predictions for the years right after training."""
        ...

    def fitted_values(self):
        """In-sample fitted values over the training years."""
        return self.fitted_


class LinearTrendForecaster(Forecaster):
    """Ordinary least-squares linear trend: pop = a*year + b."""

    def fit(self, years, values):
        self.years_ = np.asarray(years, dtype=float)
        self.values_ = np.asarray(values, dtype=float)
        self.coeffs_ = np.polyfit(self.years_, self.values_, deg=1)
        self.fitted_ = np.polyval(self.coeffs_, self.years_)
        return self

    def predict(self, horizon):
        future_years = self.years_[-1] + np.arange(1, horizon + 1)
        return np.polyval(self.coeffs_, future_years)


class ExponentialCAGRForecaster(Forecaster):
    """Compound growth: pop_t = pop_0 * (1+r)^t, r = CAGR of the training window."""

    def fit(self, years, values):
        self.years_ = np.asarray(years, dtype=float)
        self.values_ = np.asarray(values, dtype=float)
        n_periods = len(values) - 1
        self.r_ = (values[-1] / values[0]) ** (1 / n_periods) - 1
        t = np.arange(len(values))
        self.fitted_ = values[0] * (1 + self.r_) ** t
        return self

    def predict(self, horizon):
        t = np.arange(1, horizon + 1)
        return self.values_[-1] * (1 + self.r_) ** t


class FibonacciRatioForecaster(Forecaster):
    """Toy model (from a previous cohort): scales the last observed value by
    successive Fibonacci ratios F(k+1)/F(k) instead of an estimated growth
    rate. Kept for comparison / critique only."""

    def _fib_ratios(self, k):
        fib = [1, 1]
        while len(fib) < k + 2:
            fib.append(fib[-1] + fib[-2])
        return [fib[i + 1] / fib[i] for i in range(1, k + 1)]

    def fit(self, years, values):
        self.years_ = np.asarray(years, dtype=float)
        self.values_ = np.asarray(values, dtype=float)
        ratios = self._fib_ratios(len(values) - 1)
        fitted = [values[0]]
        for r in ratios:
            fitted.append(fitted[-1] * r)
        self.fitted_ = np.array(fitted)
        return self

    def predict(self, horizon):
        preds = []
        last = self.values_[-1]
        for r in self._fib_ratios(horizon):
            last = last * r
            preds.append(last)
        return np.array(preds)


MODEL_CLASSES = {
    "Linear trend": LinearTrendForecaster,
    "Exponential/CAGR": ExponentialCAGRForecaster,
    "Fibonacci-ratio": FibonacciRatioForecaster,
}
