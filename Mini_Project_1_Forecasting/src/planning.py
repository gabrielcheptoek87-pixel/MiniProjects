"""Classroom-capacity planning."""

import numpy as np

SCHOOL_AGE_SHARE = 0.18
PUPILS_PER_CLASSROOM = 53


def classrooms_needed(pop_thousands, share=SCHOOL_AGE_SHARE, per_room=PUPILS_PER_CLASSROOM):
    return int(np.ceil(pop_thousands * 1000 * share / per_room))


def classroom_plan(districts, forecasts, share=SCHOOL_AGE_SHARE, per_room=PUPILS_PER_CLASSROOM):
    """Additional classrooms needed by the last forecast year, per district."""
    results = {}
    for name, d in districts.items():
        pop_now, pop_end = d.populations[-1], forecasts[name][-1]
        rooms_now = classrooms_needed(pop_now, share, per_room)
        rooms_end = classrooms_needed(pop_end, share, per_room)
        results[name] = {
            "pop_2024": pop_now, "pop_2029": pop_end,
            "rooms_2024": rooms_now, "rooms_2029": rooms_end,
            "additional": rooms_end - rooms_now,
        }
    return results
