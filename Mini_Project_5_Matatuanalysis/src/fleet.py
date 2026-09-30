"""Fleet sizing."""
import math

TRIPS_PER_DAY = 8
SEATS_PER_VEHICLE = 14
BUFFER = 0.15


def vehicles_needed(forecast_pax: float, trips_per_day=TRIPS_PER_DAY,
                    seats=SEATS_PER_VEHICLE, buffer=BUFFER) -> dict:
    capacity = trips_per_day * seats
    buffered = forecast_pax * (1 + buffer)
    return {"forecast_pax": forecast_pax, "buffered_pax": buffered,
            "capacity_per_vehicle": capacity, "vehicles": math.ceil(buffered / capacity)}
