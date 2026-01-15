"""Evaluation pipeline for RF ML models."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from rf_research.config import RFConfig
from rf_research.data import load_or_generate_dataset
from rf_research.metrics import classification_report, format_report
from rf_research.model import SoftmaxModel, evaluate_accuracy
from rf_research.preprocessing import StandardScaler, train_test_split
from rf_research.reporting import write_json, write_markdown_summary
from rf_research.validation import raise_if_invalid


def evaluate_model(config: RFConfig) -> Dict[str, object]:
    dataset = load_or_generate_dataset(config)
    raise_if_invalid(dataset.features, dataset.labels)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(dataset.features)
    _, x_test, _, y_test = train_test_split(
        scaled, dataset.labels, config.train_ratio, config.seed
    )
    model = SoftmaxModel.load(config.model_path)
    predictions = model.predict(x_test)
    accuracy = evaluate_accuracy(model, x_test, y_test)
    report = classification_report(y_test, predictions)
    return {
        "accuracy": accuracy,
        "samples": len(x_test),
        "model_path": str(config.model_path),
        "precision": report.precision,
        "recall": report.recall,
        "f1_score": report.f1_score,
        "support": report.support,
        "summary": format_report(report),
    }


def save_evaluation_report(report: Dict[str, object], path: Path) -> None:
    write_json(report, path)
    markdown_path = path.with_suffix(".md")
    write_markdown_summary(report, markdown_path)
