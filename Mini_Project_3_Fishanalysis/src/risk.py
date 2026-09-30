"""Dispersion statistics, CV-based risk classifier, and Value-at-Risk."""
import statistics

import numpy as np


def revenue_stats(revenues):
    """Mean, median, variance, sd and coefficient of variation of a revenue series."""
    mean = statistics.mean(revenues)
    return {
        "mean": mean,
        "median": statistics.median(revenues),
        "variance": statistics.variance(revenues),
        "sd": statistics.stdev(revenues),
        "cv": statistics.stdev(revenues) / mean if mean else float("inf"),
    }


class RiskAssessor:
    """Classify risk using the coefficient of variation (CV = sd/mean), a
    dimensionless measure -- unlike raw variance, which is in UGX^2 and depends
    on the size of the operation."""

    BANDS = [
        (0.10, "Low"),
        (0.20, "Moderate"),
        (0.35, "High"),
        (float("inf"), "Severe"),
    ]

    @classmethod
    def classify(cls, cv):
        for threshold, label in cls.BANDS:
            if cv <= threshold:
                return label
        return "Severe"

    @staticmethod
    def value_at_risk(totals, level=0.05):
        """Return (VaR cutoff revenue, shortfall of that cutoff below the mean)."""
        cutoff = np.percentile(totals, level * 100)
        return cutoff, np.mean(totals) - cutoff
