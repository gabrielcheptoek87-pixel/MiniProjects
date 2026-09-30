"""Forecaster base class and concrete models."""
from abc import ABC, abstractmethod

import numpy as np


class Forecaster(ABC):
    """Fit on a 1D history array, then forecast the next value."""

    @abstractmethod
    def fit(self, history: np.ndarray):
        ...

    @abstractmethod
    def forecast_next(self) -> float:
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__


class MovingAverageForecaster(Forecaster):
    def __init__(self, window: int = 3):
        self.window = window

    def fit(self, history):
        self.history = np.asarray(history, dtype=float)
        return self

    def forecast_next(self) -> float:
        w = min(self.window, len(self.history))
        return float(self.history[-w:].mean())

    @property
    def name(self) -> str:
        return f"MovingAverage({self.window})"


class ExponentialSmoothingForecaster(Forecaster):
    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha

    def fit(self, history):
        history = np.asarray(history, dtype=float)
        level = history[0]
        for x in history[1:]:
            level = self.alpha * x + (1 - self.alpha) * level
        self.level = level
        return self

    def forecast_next(self) -> float:
        return float(self.level)

    @property
    def name(self) -> str:
        return f"SES(alpha={self.alpha:.1f})"


class LinearTrendForecaster(Forecaster):
    def fit(self, history):
        history = np.asarray(history, dtype=float)
        t = np.arange(len(history))
        A = np.vstack([t, np.ones_like(t)]).T
        self.slope, self.intercept = np.linalg.lstsq(A, history, rcond=None)[0]
        self.n = len(history)
        return self

    def forecast_next(self) -> float:
        return float(self.slope * self.n + self.intercept)

    @property
    def name(self) -> str:
        return "LinearTrend"


class SeasonalNaiveForecaster(Forecaster):
    """Forecast = value from one season (default 7 days) ago."""

    def __init__(self, period: int = 7):
        self.period = period

    def fit(self, history):
        self.history = np.asarray(history, dtype=float)
        return self

    def forecast_next(self) -> float:
        if len(self.history) < self.period:
            return float(self.history[-1])  # fallback until a full cycle exists
        return float(self.history[-self.period])

    @property
    def name(self) -> str:
        return f"SeasonalNaive({self.period})"
