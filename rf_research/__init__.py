"""RF Research toolkit for local, reproducible experiments."""

from rf_research.config import RFConfig
from rf_research.data import generate_synthetic_dataset
from rf_research.training import train_and_save
from rf_research.evaluation import evaluate_model

__all__ = [
    "RFConfig",
    "generate_synthetic_dataset",
    "train_and_save",
    "evaluate_model",
]
