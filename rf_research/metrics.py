"""Metrics utilities for classification tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ClassificationReport:
    precision: Dict[int, float]
    recall: Dict[int, float]
    f1_score: Dict[int, float]
    support: Dict[int, int]
    accuracy: float


def confusion_matrix(labels: List[int], predictions: List[int], num_classes: int) -> List[List[int]]:
    matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
    for true_label, pred_label in zip(labels, predictions):
        matrix[int(true_label)][int(pred_label)] += 1
    return matrix


def classification_report(labels: List[int], predictions: List[int]) -> ClassificationReport:
    num_classes = max(max(labels, default=0), max(predictions, default=0)) + 1
    matrix = confusion_matrix(labels, predictions, num_classes)
    precision = {}
    recall = {}
    f1_score = {}
    support = {}

    for cls in range(num_classes):
        tp = matrix[cls][cls]
        fp = sum(matrix[row][cls] for row in range(num_classes)) - tp
        fn = sum(matrix[cls]) - tp
        precision_val = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall_val = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_val = (
            2 * precision_val * recall_val / (precision_val + recall_val)
            if (precision_val + recall_val) > 0
            else 0.0
        )
        precision[cls] = float(precision_val)
        recall[cls] = float(recall_val)
        f1_score[cls] = float(f1_val)
        support[cls] = int(sum(matrix[cls]))

    accuracy = (
        sum(1 for label, pred in zip(labels, predictions) if label == pred) / len(labels)
        if labels
        else 0.0
    )
    return ClassificationReport(
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        support=support,
        accuracy=accuracy,
    )


def format_report(report: ClassificationReport) -> List[str]:
    lines = ["class precision recall f1 support"]
    for cls in sorted(report.support.keys()):
        lines.append(
            f"{cls:>5} {report.precision[cls]:>9.3f} {report.recall[cls]:>6.3f} "
            f"{report.f1_score[cls]:>5.3f} {report.support[cls]:>7}"
        )
    lines.append(f"accuracy: {report.accuracy:.3f}")
    return lines
