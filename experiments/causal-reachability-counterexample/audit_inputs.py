"""Print aggregate schema and support diagnostics from four local study files."""

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read(path, delimiter=","):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source, delimiter=delimiter))


def observed(value):
    return value not in ("", "NA", "NaN")


def shape(rows, *key):
    return {
        "rows": len(rows),
        "participants": len({row[key[0]] for row in rows}),
        "unique_keys": len({tuple(row[field] for field in key) for row in rows}),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("geschwind_series", "geschwind_static", "sicorello", "heartsteps"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    series = read(args.geschwind_series, "\t")
    static = read(args.geschwind_static, "\t")
    sicorello = read(args.sicorello)
    heartsteps = read(args.heartsteps)

    arms = defaultdict(set)
    for row in static:
        if observed(row["therapy"]):
            arms[row["id"]].add(row["therapy"])
    arm_support = Counter(
        "/".join(sorted(arms[person])) or "missing"
        for person in {row["id"] for row in series}
    )
    available = [row for row in heartsteps if row["avail"] == "True"]
    report = {
        "geschwind_series": {
            **shape(series, "id", "study_period", "day", "beep"),
            "keys_ignoring_period": shape(series, "id", "day", "beep")["unique_keys"],
            "missing_beep": sum(not observed(row["beep"]) for row in series),
            "cheerful_observed_by_period": Counter(
                row["study_period"] for row in series if observed(row["cheerful"])
            ),
            "pleasantness_observed": sum(observed(row["pleasantness"]) for row in series),
        },
        "geschwind_static": {
            **shape(static, "id"),
            "therapy_values_per_series_participant": arm_support,
        },
        "sicorello": {
            **shape(sicorello, "PARTICIPANT_ID", "DayInd", "OccInd"),
            "complete_scheduled_and_completed_times": sum(
                observed(row["SCHEDULED_TS"]) and observed(row["COMPLETED_TS"])
                for row in sicorello
            ),
            "support_seeking_urge": Counter(row["IMPULS.IER"] for row in sicorello),
            "self_regulation_urge": Counter(row["IMPULS.ER"] for row in sicorello),
        },
        "heartsteps": {
            **shape(heartsteps, "user.index", "decision.index"),
            "available": len(available),
            "available_randomized_flag_and_send": Counter(
                "/".join((row["is.randomized"], row["send"])) for row in available
            ),
            "available_missing_steps_by_send": Counter(
                row["send"] for row in available if not observed(row["jbsteps30"])
            ),
            "available_missing_zero_filled_steps": sum(
                not observed(row["jbsteps30.zero"]) for row in available
            ),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
