"""Rainy-season detection on a circular monthly series."""
import numpy as np
from scipy.signal import find_peaks

from .data import MONTHS


def detect_seasons(region, height_frac=0.6, min_distance=2):
    """Indices (0-11) of rainy-season peaks.

    The series is tripled so peaks spanning Dec-Jan are found; height
    threshold = height_frac * annual mean so only genuine seasonal peaks
    count.
    """
    rain = region.rainfall
    extended = np.concatenate([rain, rain, rain])
    peaks, _ = find_peaks(extended, height=height_frac * rain.mean(),
                          distance=min_distance)
    return sorted({int(p) - 12 for p in peaks if 12 <= p < 24})


def classify_modality(region):
    """(modality label, list of peak month names)."""
    peaks = detect_seasons(region)
    n = len(peaks)
    modality = "Unimodal" if n <= 1 else ("Bimodal" if n == 2 else f"{n}-modal")
    return modality, [MONTHS[p] for p in peaks]
