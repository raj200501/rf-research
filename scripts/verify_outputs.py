"""Smoke test verification for generated artifacts."""

from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = REPO_ROOT / "outputs"
MODELS = REPO_ROOT / "models"
DATA = REPO_ROOT / "data"

required_files = [
    DATA / "radio_frequencies.csv",
    OUTPUTS / "processed_radio_frequencies.csv",
    OUTPUTS / "signal_strength_summary.csv",
    OUTPUTS / "rf_collection.json",
    OUTPUTS / "rf_analysis.json",
    OUTPUTS / "evaluation_report.json",
    MODELS / "rfml_model.json",
]

missing = [str(path) for path in required_files if not path.exists()]
if missing:
    print("Missing expected output files:")
    for path in missing:
        print(f" - {path}")
    sys.exit(1)

with (OUTPUTS / "rf_analysis.json").open("r") as handle:
    report = json.load(handle)

if report.get("samples") != 10:
    print("Unexpected analysis samples count:", report.get("samples"))
    sys.exit(1)

print("Smoke verification passed.")
