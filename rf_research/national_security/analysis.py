"""Local RF data analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from rf_research.config import RFConfig


def analyze_collection(path: Path) -> Dict[str, object]:
    with path.open("r") as handle:
        data = json.load(handle)
    strengths = [float(value) for value in data["signal_strength"]]
    frequencies = [float(value) for value in data["frequency_hz"]]
    mean_strength = sum(strengths) / len(strengths) if strengths else 0.0
    peak_strength = max(strengths) if strengths else 0.0
    mean_frequency = sum(frequencies) / len(frequencies) if frequencies else 0.0
    return {
        "mean_strength": mean_strength,
        "peak_strength": peak_strength,
        "mean_frequency": mean_frequency,
        "samples": len(strengths),
    }


def save_analysis(report: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)


def analyze_and_save(config: RFConfig) -> Path:
    report = analyze_collection(config.collection_path)
    save_analysis(report, config.analysis_path)
    return config.analysis_path
