# District population forecasting

Run `district_forecasting.ipynb` (from the project root). It is the only notebook;
all reusable logic is in `src/` and imported into it.

| Module | Contents |
|---|---|
| `src/population.py` | `DistrictPopulation`, source data, `load_districts()` |
| `src/stats.py` | descriptive stats (statistics vs NumPy), YoY growth, CAGR |
| `src/models.py` | `Forecaster` ABC + Linear, Exponential/CAGR, Fibonacci-ratio |
| `src/validation.py` | MAE/RMSE/MAPE, train/test validation, final forecasts |
| `src/planning.py` | classroom-need calculation |
| `src/bootstrap.py` | bootstrap prediction intervals |
| `src/plotting.py` | combined forecast figure |

The notebook writes `outputs/district_forecasts.png`.
