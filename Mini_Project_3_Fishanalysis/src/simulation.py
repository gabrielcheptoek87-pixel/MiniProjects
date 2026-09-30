"""Monte Carlo revenue simulation and harvest-rate scenario analysis."""
import numpy as np

from .price import PRICE_WEEKLY_SD, simulate_price_path
from .risk import RiskAssessor, revenue_stats
from .stock import FishStock, msy_benchmarks

RNG_SEED = 42


def monte_carlo_annual_revenue(h, weeks=52, n_paths=2000, seed=RNG_SEED,
                               closed_weeks_per_year=0):
    """Stock path is deterministic given h (fixed harvest policy); price paths
    are randomised. Returns (revenue totals per path, weekly harvests, stock history)."""
    stock = FishStock()
    harvests = stock.simulate(weeks, h, closed_weeks_per_year)
    harvest_kg = np.array(harvests) * 1000.0
    rng = np.random.default_rng(seed)
    totals = np.empty(n_paths)
    for i in range(n_paths):
        shocks = rng.normal(0, PRICE_WEEKLY_SD, size=weeks)
        totals[i] = np.sum(harvest_kg * simulate_price_path(shocks))
    return totals, harvests, stock.history


def run_scenarios(harvest_rates, weeks=52, n_paths=2000):
    """Run each harvest rate; return (results dict, MSY, harvest rate at MSY)."""
    msy, h_at_msy = msy_benchmarks()
    results = {}
    for h in harvest_rates:
        totals, harvests, history = monte_carlo_annual_revenue(
            h, weeks=weeks, n_paths=n_paths)
        stats_ = revenue_stats(totals.tolist())
        var_cut, var_loss = RiskAssessor.value_at_risk(totals)
        results[h] = {
            "final_stock": history[-1],
            "total_harvest_tonnes": sum(harvests),
            "mean_annual_revenue": stats_["mean"],
            "cv": stats_["cv"],
            "risk_class": RiskAssessor.classify(stats_["cv"]),
            "var_5pct": var_cut,
            "var_shortfall": var_loss,
            "history": history,
            "steady_state_harvest_wk": harvests[-1],
        }
    return results, msy, h_at_msy


def closed_season_comparison(h=0.20, years=5, closed_weeks=8, n_paths=1500):
    """Compare open harvesting with an annual closed season over a multi-year horizon."""
    weeks = 52 * years
    t_open, _, hist_open = monte_carlo_annual_revenue(h, weeks, n_paths)
    t_closed, _, hist_closed = monte_carlo_annual_revenue(
        h, weeks, n_paths, closed_weeks_per_year=closed_weeks)
    return {
        "final_stock_open": hist_open[-1],
        "final_stock_closed": hist_closed[-1],
        "mean_revenue_open": float(np.mean(t_open)),
        "mean_revenue_closed": float(np.mean(t_closed)),
        "revenue_change_pct": float((np.mean(t_closed) - np.mean(t_open)) / np.mean(t_open) * 100),
        "stock_change_pct": float((hist_closed[-1] - hist_open[-1]) / hist_open[-1] * 100),
    }
