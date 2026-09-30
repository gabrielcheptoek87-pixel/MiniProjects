"""Illustrative monthly rainfall data and the Region class.

The series below are the ILLUSTRATIVE figures from the task brief, not
measured station data. Replace with NASA POWER / UNMA records before any
figure is used for real planting decisions.
"""
import numpy as np

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

RAINFALL_DATA = {
    "Kampala": [120, 140, 180, 200, 220, 180, 90, 70, 60, 100, 110, 130],
    "Gulu":    [8, 25, 75, 160, 190, 145, 170, 215, 175, 150, 60, 15],
    "Mbarara": [70, 85, 120, 140, 90, 25, 20, 55, 100, 125, 120, 90],
}


class Region:
    """Holds one region's monthly rainfall (mm) and derived statistics."""

    def __init__(self, name, monthly_mm):
        self.name = name
        self.rainfall = np.asarray(monthly_mm, dtype=float)
        if self.rainfall.shape != (12,):
            raise ValueError("Expected exactly 12 monthly values")

    def annual_total(self):
        """Total annual rainfall (mm)."""
        return float(self.rainfall.sum())

    def mean(self):
        """Mean monthly rainfall (mm)."""
        return float(self.rainfall.mean())

    def wettest_month(self):
        """(month_name, value) for the wettest month."""
        idx = int(np.argmax(self.rainfall))
        return MONTHS[idx], float(self.rainfall[idx])

    def driest_month(self):
        """(month_name, value) for the driest month."""
        idx = int(np.argmin(self.rainfall))
        return MONTHS[idx], float(self.rainfall[idx])

    def coefficient_of_variation(self):
        """CV (%) = 100 * population_std / mean.

        High CV = sharply seasonal (or erratic) regime; low CV = rainfall
        spread evenly through the year.
        """
        return float(100.0 * self.rainfall.std(ddof=0) / self.rainfall.mean())

    def __repr__(self):
        return f"Region({self.name!r}, total={self.annual_total():.0f}mm)"


REGIONS = {name: Region(name, vals) for name, vals in RAINFALL_DATA.items()}


def region_summary(regions=None):
    """Return a list of dicts (one per region) suitable for a DataFrame."""
    regions = regions or REGIONS
    rows = []
    for name, r in regions.items():
        wm, wv = r.wettest_month()
        dm, dv = r.driest_month()
        rows.append({
            "Region": name,
            "Annual total (mm)": r.annual_total(),
            "Mean monthly (mm)": round(r.mean(), 1),
            "Wettest month": f"{wm} ({wv:.0f})",
            "Driest month": f"{dm} ({dv:.0f})",
            "CV (%)": round(r.coefficient_of_variation(), 1),
        })
    return rows
