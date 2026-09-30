"""Price model: seeded, bounded random walk (UGX/kg)."""
import random

import numpy as np

PRICE_START = 12_000.0
PRICE_LOW = 9_000.0
PRICE_HIGH = 16_000.0
PRICE_WEEKLY_SD = 400.0


class PriceModel:
    def __init__(self, start=PRICE_START, low=PRICE_LOW, high=PRICE_HIGH,
                 weekly_sd=PRICE_WEEKLY_SD, seed=None):
        self.price = start
        self.low = low
        self.high = high
        self.weekly_sd = weekly_sd
        self.rng = random.Random(seed)

    def step(self):
        shock = self.rng.gauss(0, self.weekly_sd)
        self.price = min(max(self.price + shock, self.low), self.high)
        return self.price

    def simulate(self, weeks):
        return [self.step() for _ in range(weeks)]


def simulate_price_path(shocks, start=PRICE_START, low=PRICE_LOW, high=PRICE_HIGH):
    """Bounded random walk driven by a pre-drawn array of shocks."""
    price = start
    prices = np.empty(len(shocks))
    for t, shock in enumerate(shocks):
        price = min(max(price + shock, low), high)
        prices[t] = price
    return prices


def weekly_revenue(harvest_tonnes, prices_per_kg):
    """harvest in tonnes, price in UGX/kg -> revenue in UGX."""
    return [h * 1000 * p for h, p in zip(harvest_tonnes, prices_per_kg)]
