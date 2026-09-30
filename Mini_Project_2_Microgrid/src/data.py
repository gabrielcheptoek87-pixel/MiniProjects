"""Demand-data input: interactive prompts, seeded CSV generation, loading."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import RNG_SEED


def prompt_positive_float(prompt_text):
    """Robustly prompt for a non-negative number; re-prompt on bad input."""
    while True:
        raw = input(prompt_text).strip()
        if raw == "":
            print("  Value cannot be empty. Please try again.")
            continue
        try:
            val = float(raw)
        except ValueError:
            print("  That is not a valid number. Please try again.")
            continue
        if val < 0:
            print("  Value cannot be negative. Please try again.")
            continue
        return val


def interactive_single_day():
    """Interactively collect one day's D1, D2 with validation."""
    print("Enter today's demand figures for the Kasese health-centre micro-grid:")
    d1 = prompt_positive_float("  Daytime load D1 (kWh): ")
    d2 = prompt_positive_float("  Critical-equipment load D2 (kWh): ")
    return d1, d2


def generate_demand_csv(path, n_days=30, seed=RNG_SEED):
    """
    Create n_days of demand data with a weekly pattern + noise (seeded).

    Weekdays: busier clinic -> higher daytime load. Weekends: quieter.
    Critical-equipment load stays fairly constant with mild noise.
    """
    rng = np.random.default_rng(seed)
    days = np.arange(n_days)
    weekday = days % 7  # 0=Mon ... 6=Sun

    base_D1 = np.where(weekday < 5, 42.0, 30.0)
    base_D2 = np.where(weekday < 5, 25.0, 21.0)

    noise1 = rng.normal(0, 3.0, n_days)
    noise2 = rng.normal(0, 1.5, n_days)

    D1 = np.clip(base_D1 + noise1, 5, None).round(2)
    D2 = np.clip(base_D2 + noise2, 5, None).round(2)

    df = pd.DataFrame({
        "day": days + 1,
        "weekday": weekday,
        "D1_daytime_kWh": D1,
        "D2_critical_kWh": D2,
    })
    df.to_csv(path, index=False)
    return df


def load_demand_csv(path):
    return pd.read_csv(path)


def demand_matrix(df):
    """Stack D1, D2 into the (2, n) right-hand-side array the solvers expect."""
    return np.vstack([df["D1_daytime_kWh"].to_numpy(),
                      df["D2_critical_kWh"].to_numpy()])
