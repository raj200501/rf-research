"""Configuration defaults for RF research workflows."""

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"


@dataclass(frozen=True)
class RFConfig:
    """Paths and parameters used by the RF workflows."""

    data_path: Path = DATA_DIR / "radio_frequencies.csv"
    processed_path: Path = OUTPUT_DIR / "processed_radio_frequencies.csv"
    model_path: Path = MODELS_DIR / "rfml_model.json"
    report_path: Path = OUTPUT_DIR / "evaluation_report.json"
    collection_path: Path = OUTPUT_DIR / "rf_collection.json"
    analysis_path: Path = OUTPUT_DIR / "rf_analysis.json"

    samples: int = 512
    features: int = 6
    classes: int = 4
    train_ratio: float = 0.8
    seed: int = 42

    learning_rate: float = 0.05
    epochs: int = 50
    batch_size: int = 64

    def ensure_directories(self) -> None:
        """Ensure output directories exist."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
