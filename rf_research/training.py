"""Training pipeline for RF ML models."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from rf_research.config import RFConfig
from rf_research.data import Dataset, load_or_generate_dataset, summarize_dataset
from rf_research.model import train_softmax
from rf_research.preprocessing import StandardScaler, train_test_split
from rf_research.reporting import summarize_losses, write_json, write_markdown_summary
from rf_research.validation import raise_if_invalid


def train_and_save(config: RFConfig) -> Dict[str, object]:
    config.ensure_directories()
    dataset = load_or_generate_dataset(config)
    raise_if_invalid(dataset.features, dataset.labels)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(dataset.features)
    x_train, x_test, y_train, y_test = train_test_split(
        scaled, dataset.labels, config.train_ratio, config.seed
    )
    model, metrics = train_softmax(
        x_train,
        y_train,
        learning_rate=config.learning_rate,
        epochs=config.epochs,
        batch_size=config.batch_size,
        seed=config.seed,
    )
    model.save(config.model_path)
    losses = summarize_losses(metrics.losses)
    report = {
        "dataset": summarize_dataset(dataset),
        "train_accuracy": metrics.accuracy,
        **losses,
        "model_path": str(config.model_path),
    }
    return report


def save_training_report(report: Dict[str, object], path: Path) -> None:
    write_json(report, path)
    markdown_path = path.with_suffix(".md")
    write_markdown_summary(report, markdown_path)
