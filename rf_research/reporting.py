"""Reporting utilities for RF workflows."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable


def write_json(report: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)


def write_markdown_summary(report: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# RF Workflow Report", ""]
    for key, value in report.items():
        lines.append(f"- **{key}**: {value}")
    lines.append("")
    path.write_text("\n".join(lines))


def summarize_losses(losses: Iterable[float]) -> Dict[str, float]:
    values = list(losses)
    if not values:
        return {"loss_mean": 0.0, "loss_final": 0.0}
    return {"loss_mean": float(sum(values) / len(values)), "loss_final": float(values[-1])}
