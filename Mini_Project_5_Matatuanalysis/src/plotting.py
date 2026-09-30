"""Plot helpers. Each returns the Figure and optionally saves it."""
import matplotlib.pyplot as plt
import numpy as np


def _save(fig, path):
    if path:
        fig.savefig(path, dpi=150)


def plot_forecast_vs_actual(routes, forecasts, best_models, save_path=None):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, (name, route) in zip(axes, routes.items()):
        days = np.arange(1, len(route.passenger_counts) + 1)
        actual = route.daily_revenue()
        f_rev = forecasts[name] * route.fare
        nxt = days[-1] + 1
        ax.plot(days, actual, "o-", color="#2563eb", label="Actual revenue")
        ax.plot([nxt], [f_rev], "o", color="#dc2626", markersize=9,
                label=f"Day-{nxt} forecast\n({best_models[name]})")
        ax.plot([days[-1], nxt], [actual[-1], f_rev], "--", color="#dc2626", linewidth=1)
        ax.set(title=name, xlabel="Day", ylabel="Revenue (UGX)")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    fig.suptitle(f"Actual Daily Revenue (Days 1-{days[-1]}) vs Day-{nxt} Forecast", fontsize=13)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_seasonality(counts, ma_mae, sn_mae, save_path=None):
    days = np.arange(len(counts))
    weekday = days % 7
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    ax = axes[0]
    ax.plot(days, counts, "o-", color="#2563eb", markersize=3, linewidth=1)
    for d in days:
        if weekday[d] == 4:
            ax.axvspan(d - 0.5, d + 0.5, color="#fca5a5", alpha=0.3)
        if weekday[d] == 6:
            ax.axvspan(d - 0.5, d + 0.5, color="#bfdbfe", alpha=0.3)
    ax.set(title=f"Simulated {len(counts)}-day passenger counts (red=Fri, blue=Sun)",
           xlabel="Day", ylabel="Passengers")
    ax.grid(alpha=0.3)

    ax = axes[1]
    bars = ax.bar(["MovingAverage(3)", "SeasonalNaive(7)"], [ma_mae, sn_mae],
                  color=["#f59e0b", "#16a34a"])
    ax.set(ylabel="MAE (passengers/day)",
           title=f"Backtest MAE: Moving Average vs Seasonal-Naive (days 8-{len(counts)})")
    for bar, mae in zip(bars, [ma_mae, sn_mae]):
        ax.text(bar.get_x() + bar.get_width() / 2, mae + 0.1, f"{mae:.2f}", ha="center")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    _save(fig, save_path)
    return fig
