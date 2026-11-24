"""Backtest three monthly forecasts with expanding training windows."""

import argparse
import csv
import json
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


LABELS = {"seasonal_naive": "Previous year", "month_mean": "Historical month mean",
          "seasonal_trend": "Month effects + trend"}
COLORS = {"seasonal_naive": "#B45215", "month_mean": "#087B73", "seasonal_trend": "#1767A0"}


def load_months(path, date_col, value_col):
    observations = []
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not {date_col, value_col} <= set(reader.fieldnames or []):
            raise ValueError(f"Missing column: expected {date_col!r} and {value_col!r}")
        for row in reader:
            stamp = row[date_col].strip()
            day = date.fromisoformat(stamp + "-01" if len(stamp) == 7 else stamp)
            observations.append((day.replace(day=1), float(row[value_col])))
    observations.sort()
    if not observations:
        raise ValueError("Monthly data are empty")
    dates, values = zip(*observations)
    ordinal = np.array([day.year * 12 + day.month - 1 for day in dates])
    if (np.diff(ordinal) != 1).any() or not np.isfinite(values).all():
        raise ValueError("Expected one finite observation per consecutive calendar month")
    return dates, np.array(values), ordinal % 12


def backtest(values, months, folds, horizon):
    origin = len(values) - folds * horizon
    if min(folds, horizon) < 1 or origin < 24:
        raise ValueError("Provide positive folds and horizon with at least 24 initial training months")
    trace = {name: [] for name in LABELS}
    fold_mae = {name: [] for name in LABELS}
    monthly = np.eye(12)[months]
    design = np.column_stack((monthly, np.arange(len(values)) / 12))
    for start in range(origin, len(values), horizon):
        test = slice(start, start + horizon)
        train = values[:start]
        mean_by_month = np.bincount(months[:start], weights=train, minlength=12) / monthly[:start].sum(axis=0)
        coeff, *_ = np.linalg.lstsq(design[:start], train, rcond=None)
        forecast = {"seasonal_naive": train[-12:][np.arange(horizon) % 12],
                    "month_mean": mean_by_month[months[test]], "seasonal_trend": design[test] @ coeff}
        for name, prediction in forecast.items():
            trace[name].extend(prediction)
            fold_mae[name].append(float(np.mean(np.abs(values[test] - prediction))))
    return origin, {name: np.array(y) for name, y in trace.items()}, fold_mae


def plot(output, dates, actual, predictions, fold_mae, unit, fold_starts):
    fig, (upper, lower) = plt.subplots(2, 1, height_ratios=(2, 1), figsize=(8, 5.4), layout="constrained")
    upper.plot(dates, actual, color="#242E38", lw=1.8, label="Observed", zorder=4)
    for name, style in zip(LABELS, ("--", ":", "-.")):
        upper.plot(dates, predictions[name], color=COLORS[name], ls=style, lw=1.3, label=LABELS[name])
        lower.plot(fold_starts, fold_mae[name], color=COLORS[name], ls=style, marker="o", ms=4)
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    upper.xaxis.set_major_locator(locator)
    upper.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    upper.set_ylabel(f"Observed / forecast ({unit})")
    upper.legend(loc="lower left", bbox_to_anchor=(0, 1.02), frameon=False, ncols=2)
    lower.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=2, maxticks=7))
    lower.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    if len(fold_starts) <= 8:
        lower.set_xticks(fold_starts)
    lower.set_xlabel("First forecast month of each fold")
    lower.set_ylabel(f"Fold MAE ({unit})")
    lower.set_ylim(bottom=0)
    for ax in (upper, lower):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.23)
    fig.savefig(output / "backtest.png", dpi=200)
    fig.savefig(output / "backtest.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--date", required=True, help="Month column in YYYY-MM or ISO date format")
    parser.add_argument("--value", required=True)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--horizon", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    dates, values, months = load_months(args.csv, args.date, args.value)
    origin, predictions, fold_mae = backtest(values, months, args.folds, args.horizon)
    dates, actual = dates[origin:], values[origin:]
    scores = {}
    for name, prediction in predictions.items():
        error = prediction - actual
        scores[name] = {"mae": float(np.mean(np.abs(error))), "rmse": float(np.sqrt(np.mean(error**2))),
                        "bias": float(np.mean(error)), "mae_by_fold": fold_mae[name]}
    summary = {"first_test_month": dates[0].isoformat()[:7], "last_test_month": dates[-1].isoformat()[:7],
               "initial_training_months": origin, "test_months": len(actual), "unit": args.unit,
               "horizon": args.horizon, "folds": args.folds, "scores": scores}
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "predictions.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["month", "fold", "observed", *LABELS])
        for i, day in enumerate(dates):
            writer.writerow([day.isoformat()[:7], 1 + i // args.horizon, actual[i],
                             *(predictions[name][i] for name in LABELS)])
    plot(args.output, dates, actual, predictions, fold_mae, args.unit, dates[::args.horizon])
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                                              encoding="utf-8")
    brief = {name: round(scores[name]["mae"], 4) for name in LABELS}
    print(json.dumps({"test_months": len(actual), "mae": brief, "summary": str(args.output / "summary.json")},
                     ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
