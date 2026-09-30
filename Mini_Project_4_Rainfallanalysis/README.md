# Rainfall regime & crop suitability analysis

```
rainfall_project/
├── rainfall_analysis.ipynb   # the one notebook: calls src/, shows results
├── src/
│   ├── data.py         # MONTHS, RAINFALL_DATA, Region, region_summary()
│   ├── crops.py        # CropRule, CROP_RULES (with sources), classify_all()
│   ├── similarity.py   # cosine (fixed), scipy check, cosine/Pearson/Euclidean matrices
│   ├── seasonality.py  # find_peaks-based season detection
│   ├── synthetic.py    # SYNTHETIC 10-yr rainfall (placeholder for NASA POWER / UNMA)
│   └── plots.py        # line chart, suitability heatmap, box plots (return Figures)
└── figures/            # written by the notebook
```
Run Jupyter from this folder (the project root) so `import src...` resolves. Needs numpy, scipy, matplotlib >= 3.9, pandas.
