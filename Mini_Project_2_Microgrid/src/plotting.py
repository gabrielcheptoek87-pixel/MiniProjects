"""Figures. Each function returns the figure and saves it if outpath is given."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def plot_usage_and_cost(X, daily_cost, outpath=None):
    n = X.shape[1]
    days = np.arange(1, n + 1)

    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax1.bar(days, X[0], label="Solar (x)", color="#e8a33d")
    ax1.bar(days, X[1], bottom=X[0], label="Battery (y)", color="#3d6de8")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Energy dispatched (kWh)")
    ax1.set_title("Kasese micro-grid: daily solar vs battery usage & cost")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(days, daily_cost, color="black", marker="o",
             linewidth=1.5, label="Daily cost (UGX)")
    ax2.set_ylabel("Daily cost (UGX)")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    if outpath is not None:
        fig.savefig(outpath, dpi=150)
    return fig


def plot_sensitivity(X_mc, x_base, y_base, cond, outpath=None):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].hist(X_mc[0], bins=40, color="#e8a33d", alpha=0.85)
    axes[0].axvline(x_base, color="black", linestyle="--", label=f"base x={x_base:.2f}")
    axes[0].set_title("Solar (x) under +-5% demand noise")
    axes[0].set_xlabel("x (kWh)")
    axes[0].legend()

    axes[1].hist(X_mc[1], bins=40, color="#3d6de8", alpha=0.85)
    axes[1].axvline(y_base, color="black", linestyle="--", label=f"base y={y_base:.2f}")
    axes[1].set_title("Battery (y) under +-5% demand noise")
    axes[1].set_xlabel("y (kWh)")
    axes[1].legend()

    fig.suptitle(f"Monte Carlo sensitivity (1000 draws) - condition number = {cond:.2f}")
    fig.tight_layout()
    if outpath is not None:
        fig.savefig(outpath, dpi=150)
    return fig
