"""Combined forecast figure."""

import matplotlib.pyplot as plt


def plot_forecasts(districts, best_models, models, forecasts, intervals,
                   forecast_years, split_year=2021, save_path=None):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()

    for ax, (name, d) in zip(axes, districts.items()):
        model_name = best_models[name]
        ax.plot(d.years, d.populations, "o-", color="black", label="Actual", linewidth=1.5)
        ax.plot(d.years, models[name].fitted_values(), "--", color="tab:blue",
                label=f"Fitted ({model_name})")
        ax.plot(forecast_years, forecasts[name], "s--", color="tab:red", label="Forecast 2025-29")

        lower, upper = intervals[name]
        ax.fill_between(forecast_years, lower, upper, color="tab:red", alpha=0.2, label="95% PI")

        ax.axvline(split_year + 0.5, color="gray", linestyle=":", linewidth=1)
        ax.text(split_year + 0.5, ax.get_ylim()[0], " train | test",
                fontsize=7, va="bottom", color="gray")

        ax.set_title(f"{name}  (selected: {model_name})", fontsize=10)
        ax.set_xlabel("Year")
        ax.set_ylabel("Population (thousands)")
        ax.legend(fontsize=7, loc="upper left")

    for ax in axes[len(districts):]:
        ax.axis("off")

    fig.suptitle("District population: actual, fitted, and 2025-2029 forecasts", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig
