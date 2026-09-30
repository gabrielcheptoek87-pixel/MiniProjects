"""Route model and the 10-day source data."""
import statistics

import numpy as np


class Route:
    """A matatu route: daily passenger counts + fixed fare (UGX)."""

    def __init__(self, name: str, passenger_counts, fare: float):
        self.name = name
        self.passenger_counts = np.array(passenger_counts, dtype=float)
        self.fare = float(fare)

    def daily_revenue(self) -> np.ndarray:
        return self.passenger_counts * self.fare

    def total_revenue(self) -> float:
        return float(self.daily_revenue().sum())

    def descriptive_stats(self) -> dict:
        counts = list(self.passenger_counts)
        return {
            "mean": statistics.mean(counts),
            "variance": statistics.variance(counts),  # sample variance
            "stdev": statistics.stdev(counts),         # sample std dev
            "min": min(counts),
            "max": max(counts),
        }

    def __repr__(self):
        return f"Route({self.name}, fare=UGX {self.fare:,.0f})"


def load_routes() -> dict:
    """Return the three routes keyed by name."""
    return {
        "Kampala-Ntinda": Route(
            "Kampala-Ntinda", [35, 40, 42, 50, 55, 60, 48, 52, 47, 45], fare=2000),
        "Kampala-Entebbe": Route(
            "Kampala-Entebbe", [60, 58, 65, 70, 72, 80, 75, 68, 66, 64], fare=5000),
        "Kampala-Mukono": Route(
            "Kampala-Mukono", [45, 47, 50, 49, 55, 62, 58, 53, 51, 50], fare=3000),
    }
