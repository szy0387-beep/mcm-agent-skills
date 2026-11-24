"""Regression checks for the bundled monthly backtest."""

import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import numpy as np


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/mcm-fast/scripts/monthly.py"
SPEC = importlib.util.spec_from_file_location("monthly_forecast", SCRIPT)
MONTHLY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MONTHLY)


class MonthlyBacktestTests(unittest.TestCase):
    def test_months_must_be_consecutive_and_unique(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "history.csv"
            for dates in (("2021-01", "2021-03"), ("2021-01-01", "2021-01-15")):
                with self.subTest(dates=dates):
                    source.write_text(f"month,value\n{dates[0]},2\n{dates[1]},3\n", encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "one finite observation per consecutive"):
                        MONTHLY.load_months(source, "month", "value")

    def test_incomplete_csv_record_has_location(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "history.csv"
            source.write_text("month,value\n2021-01\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "CSV record 2"):
                MONTHLY.load_months(source, "month", "value")

    def test_bad_windows_fail_before_fitting(self):
        values = np.arange(40, dtype=float)
        months = np.arange(40) % 12
        for folds, horizon in ((2, 12), (0, 12), (1, 0), (-1, 4)):
            with self.subTest(folds=folds, horizon=horizon):
                with self.assertRaisesRegex(ValueError, "at least 24 initial training months"):
                    MONTHLY.backtest(values, months, folds, horizon)

    def test_long_horizon_reuses_last_observed_season_per_fold(self):
        values = np.arange(58, dtype=float)
        months = np.arange(58) % 12
        origin, predicted, errors = MONTHLY.backtest(values, months, folds=2, horizon=17)
        self.assertEqual(origin, 24)
        expected = np.r_[12:24, 12:17, 29:41, 29:34]
        np.testing.assert_array_equal(predicted["seasonal_naive"], expected)
        np.testing.assert_allclose(predicted["seasonal_trend"], values[24:], atol=1e-10)
        self.assertEqual(len(errors["seasonal_naive"]), 2)

    def test_cli_writes_reproducible_results(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "history.csv"
            records = ["month,value"]
            for index in range(37):
                year, month = divmod(index, 12)
                records.append(f"{2021 + year}-{month + 1:02d},{100 + 2 * index}")
            source.write_text("\n".join(records) + "\n", encoding="utf-8")
            out = root / "result"
            command = [sys.executable, str(SCRIPT), str(source), "--date", "month", "--value", "value",
                       "--unit", "units", "--folds", "1", "--horizon", "13", "--output", str(out)]
            subprocess.run(command, check=True, capture_output=True)
            summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual((summary["initial_training_months"], summary["test_months"]), (24, 13))
            self.assertLess(summary["scores"]["seasonal_trend"]["mae"], 1e-10)
            with (out / "predictions.csv").open(encoding="utf-8", newline="") as file:
                predicted = list(csv.DictReader(file))
            self.assertEqual(len(predicted), 13)
            self.assertEqual(float(predicted[0]["seasonal_naive"]), float(predicted[-1]["seasonal_naive"]))
            self.assertTrue((out / "backtest.pdf").read_bytes().startswith(b"%PDF-"))
            self.assertTrue((out / "backtest.png").read_bytes().startswith(b"\x89PNG"))
