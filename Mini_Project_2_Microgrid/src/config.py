"""Project-wide constants and paths."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

CSV_PATH = DATA_DIR / "demand_30days.csv"
PLOT_USAGE_PATH = OUTPUT_DIR / "daily_usage_and_cost.png"
PLOT_SENS_PATH = OUTPUT_DIR / "sensitivity_analysis.png"

RNG_SEED = 42
SOLAR_COST_UGX = 150      # UGX per kWh
BATTERY_COST_UGX = 450    # UGX per kWh
