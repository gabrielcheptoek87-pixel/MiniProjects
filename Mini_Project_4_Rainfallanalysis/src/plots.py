"""Plotting functions. Each returns a matplotlib Figure (caller saves/shows)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

from .data import MONTHS, REGIONS
from .crops import CROP_RULES, classify_all, simplify_label

REGION_COLORS = {"Kampala": "#1f77b4", "Gulu": "#d62728", "Mbarara": "#2ca02c"}
REGION_MARKERS = {"Kampala": "o", "Gulu": "s", "Mbarara": "^"}

CATEGORY_ORDER = ["Drought risk", "Marginal (wet)", "Good", "Waterlogging risk"]
CATEGORY_COLORS = {
    "Drought risk": "#d62728",
    "Marginal (wet)": "#f2c744",
    "Good": "#2ca02c",
    "Waterlogging risk": "#1f4e8c",
}


def line_chart(regions=None, title="Monthly Rainfall by Region (illustrative data)"):
    regions = regions or REGIONS
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, region in regions.items():
        ax.plot(MONTHS, region.rainfall, marker=REGION_MARKERS.get(name, "o"),
                label=name, color=REGION_COLORS.get(name), linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Rainfall (mm)")
    ax.legend(title="Region")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def suitability_heatmap(regions=None, rules=None):
    regions = regions or REGIONS
    rules = rules or CROP_RULES
    cat_to_idx = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    cmap = ListedColormap([CATEGORY_COLORS[c] for c in CATEGORY_ORDER])
    norm = BoundaryNorm(np.arange(len(CATEGORY_ORDER) + 1) - 0.5, cmap.N)

    classification = classify_all(regions, rules)
    region_names, crop_names = list(regions), list(rules)

    fig, axes = plt.subplots(len(crop_names), 1, figsize=(9, 8), sharex=True)
    for ax, crop in zip(np.atleast_1d(axes), crop_names):
        grid = np.zeros((len(region_names), 12), dtype=int)
        for i, rname in enumerate(region_names):
            for m, label in enumerate(classification[rname][crop]):
                grid[i, m] = cat_to_idx[simplify_label(label)]
        ax.imshow(grid, aspect="auto", cmap=cmap, norm=norm)
        ax.set_yticks(range(len(region_names)))
        ax.set_yticklabels(region_names)
        ax.set_title(crop.capitalize(), loc="left", fontweight="bold")
        ax.set_xticks(range(12))
        ax.set_xticklabels(MONTHS)

    handles = [Patch(color=CATEGORY_COLORS[c], label=c) for c in CATEGORY_ORDER]
    fig.legend(handles=handles, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Crop Suitability by Month and Region", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    return fig


def variability_boxplots(synthetic, title=None):
    """Box plots per month; `synthetic` maps region name -> (n_years x 12) array."""
    title = title or ("Synthetic 10-Year Monthly Rainfall Variability "
                      "(placeholder for real NASA POWER / UNMA data)")
    fig, axes = plt.subplots(1, len(synthetic), figsize=(15, 4.5), sharey=True)
    for ax, (name, data) in zip(np.atleast_1d(axes), synthetic.items()):
        ax.boxplot(data, tick_labels=MONTHS, showmeans=True)  # matplotlib >= 3.9
        ax.set_title(name)
        ax.set_xlabel("Month")
    np.atleast_1d(axes)[0].set_ylabel("Rainfall (mm)")
    fig.suptitle(title, fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    return fig
