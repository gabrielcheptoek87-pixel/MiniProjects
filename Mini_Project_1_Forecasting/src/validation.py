"""Error metrics, train/test validation and final forecasting."""

import numpy as np

from .models import MODEL_CLASSES


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def train_test_split_years(years, split_year=2021):
    years = np.asarray(years)
    return years <= split_year, years > split_year


def validate_models(districts, split_year=2021, model_classes=MODEL_CLASSES):
    """Fit every model on the train window, score on the test window.

    Returns (validation_tables, best_models) keyed by district name;
    best = lowest RMSE.
    """
    tables, best_models = {}, {}
    for name, d in districts.items():
        train_mask, test_mask = train_test_split_years(d.years, split_year)
        train_years, train_vals = d.years[train_mask], d.populations[train_mask]
        test_vals = d.populations[test_mask]

        rows = []
        for model_name, cls in model_classes.items():
            preds = cls().fit(train_years, train_vals).predict(len(test_vals))
            rows.append({
                "model": model_name,
                "MAE": mae(test_vals, preds),
                "RMSE": rmse(test_vals, preds),
                "MAPE": mape(test_vals, preds),
            })
        tables[name] = rows
        best_models[name] = min(rows, key=lambda r: r["RMSE"])["model"]
    return tables, best_models


def forecast_districts(districts, best_models, forecast_years, model_classes=MODEL_CLASSES):
    """Refit each district's selected model on all data and forecast.

    Returns (forecasts, fitted_models) keyed by district name.
    """
    forecasts, models = {}, {}
    for name, d in districts.items():
        model = model_classes[best_models[name]]().fit(d.years, d.populations)
        forecasts[name] = model.predict(len(forecast_years))
        models[name] = model
    return forecasts, models
