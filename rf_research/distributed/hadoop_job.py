"""Local MapReduce-style aggregation for RF data."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from rf_research.config import RFConfig


def aggregate_signal_strength(config: RFConfig) -> Path:
    """Aggregate signal strength per label and write summary CSV."""
    totals = defaultdict(float)
    counts = defaultdict(int)
    with config.data_path.open("r", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            label = row.get("label", "unknown")
            strength = float(row.get("feature_0", 0.0))
            totals[label] += strength
            counts[label] += 1
    output_path = config.processed_path.with_name("signal_strength_summary.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["label", "avg_signal_strength", "samples"])
        for label, total in sorted(totals.items()):
            writer.writerow([label, f"{total / counts[label]:.5f}", counts[label]])
    return output_path
