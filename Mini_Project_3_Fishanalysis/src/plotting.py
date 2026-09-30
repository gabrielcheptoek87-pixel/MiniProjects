"""Charts for the harvest & revenue risk analysis."""
import matplotlib.pyplot as plt
import numpy as np

from .risk import RiskAssessor
from .simulation import monte_carlo_annual_revenue


def plot_stock_trajectories(results, path=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    for h, r_ in results.items():
        ax.plot(r_["history"], label=f"h = {h:.2f}")
    ax.axhline(5000, color="gray", linestyle="--", linewidth=1,
               label="K/2 (MSY equilibrium, N=5,000t)")
    ax.set_xlabel("Week")
    ax.set_ylabel("Stock (tonnes)")
    ax.set_title("Fish Stock Trajectories under Different Harvest Rates (52 weeks)")
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=150)
    return fig


def plot_revenue_histogram(h=0.20, n_paths=2000, path=None):
    totals, _, _ = monte_carlo_annual_revenue(h, n_paths=n_paths)
    var_cut, _ = RiskAssessor.value_at_risk(totals)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(totals / 1e9, bins=40, color="#4C72B0", alpha=0.85)
    ax.axvline(var_cut / 1e9, color="red", linestyle="--", linewidth=2,
               label=f"5% VaR = {var_cut/1e9:.1f}B UGX")
    ax.axvline(np.mean(totals) / 1e9, color="black", linestyle=":", linewidth=1.5,
               label=f"Mean = {np.mean(totals)/1e9:.1f}B UGX")
    ax.set_xlabel("Simulated Annual Revenue (billions UGX)")
    ax.set_ylabel(f"Frequency (of {n_paths:,} simulated price paths)")
    ax.set_title(f"Distribution of Annual Revenue (h = {h}) with 5% VaR")
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=150)
    return fig
