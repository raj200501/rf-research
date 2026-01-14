"""Local Spark-like processing using pure Python."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

from rf_research.config import RFConfig


def _read_rows(path: Path) -> List[dict]:
    with path.open("r", newline="") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def _write_rows(path: Path, rows: Iterable[dict], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def process_data(config: RFConfig) -> Path:
    """Filter dataset to rows with positive signal strength."""
    rows = _read_rows(config.data_path)
    if not rows:
        raise ValueError("Dataset is empty")
    fieldnames = list(rows[0].keys())
    filtered = [
        row
        for row in rows
        if float(row.get("feature_0", 0.0)) > 0.0
    ]
    _write_rows(config.processed_path, filtered, fieldnames)
    return config.processed_path
