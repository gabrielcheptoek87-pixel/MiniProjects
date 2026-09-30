"""DistrictPopulation container and the source data."""

import numpy as np

YEARS = list(range(2015, 2025))

DISTRICTS_RAW = {
    "Kampala": [1200, 1250, 1300, 1350, 1420, 1500, 1580, 1650, 1720, 1800],
    "Wakiso":  [950, 1000, 1070, 1150, 1220, 1300, 1390, 1480, 1570, 1670],
    "Gulu":    [320, 330, 345, 360, 375, 390, 410, 430, 455, 480],
    # two additional districts (illustrative)
    "Mbale":   [480, 495, 505, 520, 535, 552, 566, 580, 596, 610],
    "Mbarara": [420, 432, 448, 462, 478, 495, 510, 528, 545, 565],
}


class DistrictPopulation:
    """Stores a district's yearly population estimates (in thousands)."""

    def __init__(self, name, years, populations):
        years = np.asarray(years, dtype=float)
        populations = np.asarray(populations, dtype=float)

        if years.shape[0] != populations.shape[0]:
            raise ValueError(
                f"{name}: years and populations must have equal length "
                f"({years.shape[0]} vs {populations.shape[0]})"
            )
        if np.any(populations < 0):
            raise ValueError(f"{name}: population values cannot be negative")
        if years.shape[0] < 2:
            raise ValueError(f"{name}: need at least 2 data points")

        self.name = name
        self.years = years
        self.populations = populations

    def __repr__(self):
        return (f"DistrictPopulation(name={self.name!r}, "
                f"years={int(self.years[0])}-{int(self.years[-1])}, "
                f"n={len(self)}, "
                f"latest={self.populations[-1]:.0f}k)")

    def __len__(self):
        return len(self.years)


def load_districts(raw=None, years=None):
    """Build {name: DistrictPopulation} from raw data (defaults to built-in)."""
    raw = DISTRICTS_RAW if raw is None else raw
    years = YEARS if years is None else years
    return {name: DistrictPopulation(name, years, pops) for name, pops in raw.items()}
