"""Local RF data collection simulation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import random

from rf_research.config import RFConfig


def collect_rf_data(config: RFConfig) -> Dict[str, object]:
    rand = random.Random(config.seed)
    timestamps = [datetime.now(timezone.utc).isoformat() for _ in range(10)]
    data = {
        "timestamp": timestamps,
        "frequency_hz": [round(rand.uniform(1e6, 3e6), 2) for _ in range(10)],
        "signal_strength": [round(rand.uniform(0.1, 1.0), 3) for _ in range(10)],
    }
    return data


def save_collection(data: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)


def collect_and_save(config: RFConfig) -> Path:
    data = collect_rf_data(config)
    save_collection(data, config.collection_path)
    return config.collection_path
