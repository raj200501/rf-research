"""Minimal multiclass logistic regression model for RF classification."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import json
import math

from rf_research.math_utils import argmax
from rf_research.random_utils import rng


@dataclass
class SoftmaxModel:
    weights: List[List[float]]
    bias: List[float]

    def predict_logits(self, features: List[List[float]]) -> List[List[float]]:
        logits = []
        for row in features:
            row_logits = []
            for class_idx in range(len(self.bias)):
                score = sum(
                    value * self.weights[feat_idx][class_idx]
                    for feat_idx, value in enumerate(row)
                ) + self.bias[class_idx]
                row_logits.append(score)
            logits.append(row_logits)
        return logits

    def predict(self, features: List[List[float]]) -> List[int]:
        logits = self.predict_logits(features)
        return [argmax(row) for row in logits]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"weights": self.weights, "bias": self.bias}
        path.write_text(json.dumps(payload))

    @classmethod
    def load(cls, path: Path) -> "SoftmaxModel":
        payload = json.loads(path.read_text())
        return cls(weights=payload["weights"], bias=payload["bias"])


@dataclass
class TrainingMetrics:
    losses: List[float]
    accuracy: float


def _softmax(logits: List[float]) -> List[float]:
    max_logit = max(logits)
    exp_logits = [math.exp(value - max_logit) for value in logits]
    total = sum(exp_logits)
    return [value / total for value in exp_logits]


def train_softmax(
    features: List[List[float]],
    labels: List[int],
    learning_rate: float,
    epochs: int,
    batch_size: int,
    seed: int,
) -> Tuple[SoftmaxModel, TrainingMetrics]:
    rand = rng(seed)
    num_samples = len(features)
    num_features = len(features[0])
    num_classes = max(labels) + 1
    weights = [[rand.gauss(0.0, 0.01) for _ in range(num_classes)] for _ in range(num_features)]
    bias = [0.0 for _ in range(num_classes)]
    losses: List[float] = []

    for _ in range(epochs):
        indices = list(range(num_samples))
        rand.shuffle(indices)
        for start in range(0, num_samples, batch_size):
            batch_idx = indices[start : start + batch_size]
            grad_w = [[0.0 for _ in range(num_classes)] for _ in range(num_features)]
            grad_b = [0.0 for _ in range(num_classes)]
            batch_loss = 0.0

            for idx in batch_idx:
                row = features[idx]
                label = labels[idx]
                logits = [
                    sum(row[feat_idx] * weights[feat_idx][class_idx] for feat_idx in range(num_features))
                    + bias[class_idx]
                    for class_idx in range(num_classes)
                ]
                probs = _softmax(logits)
                batch_loss += -math.log(probs[label] + 1e-9)
                for class_idx in range(num_classes):
                    error = probs[class_idx] - (1.0 if class_idx == label else 0.0)
                    grad_b[class_idx] += error
                    for feat_idx in range(num_features):
                        grad_w[feat_idx][class_idx] += row[feat_idx] * error

            batch_size_actual = len(batch_idx)
            if batch_size_actual == 0:
                continue
            batch_loss /= batch_size_actual
            losses.append(batch_loss)
            for feat_idx in range(num_features):
                for class_idx in range(num_classes):
                    weights[feat_idx][class_idx] -= (
                        learning_rate * grad_w[feat_idx][class_idx] / batch_size_actual
                    )
            for class_idx in range(num_classes):
                bias[class_idx] -= learning_rate * grad_b[class_idx] / batch_size_actual

    model = SoftmaxModel(weights=weights, bias=bias)
    accuracy = evaluate_accuracy(model, features, labels)
    return model, TrainingMetrics(losses=losses, accuracy=accuracy)


def evaluate_accuracy(model: SoftmaxModel, features: List[List[float]], labels: List[int]) -> float:
    predictions = model.predict(features)
    correct = sum(1 for pred, label in zip(predictions, labels) if pred == label)
    return correct / len(labels) if labels else 0.0
