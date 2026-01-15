"""Preprocessing utilities for RF datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from rf_research.math_utils import mean, std
from rf_research.random_utils import rng


@dataclass
class StandardScaler:
    """Simple feature scaler that standardizes features."""

    mean_: List[float] | None = None
    scale_: List[float] | None = None

    def fit(self, features: List[List[float]]) -> "StandardScaler":
        self.mean_ = [mean(column) for column in zip(*features)]
        self.scale_ = [std(column) for column in zip(*features)]
        self.scale_ = [value if value != 0 else 1.0 for value in self.scale_]
        return self

    def transform(self, features: List[List[float]]) -> List[List[float]]:
        if self.mean_ is None or self.scale_ is None:
            raise ValueError("Scaler has not been fitted")
        scaled = []
        for row in features:
            scaled.append(
                [
                    (value - mean_val) / scale_val
                    for value, mean_val, scale_val in zip(row, self.mean_, self.scale_)
                ]
            )
        return scaled

    def fit_transform(self, features: List[List[float]]) -> List[List[float]]:
        return self.fit(features).transform(features)


def train_test_split(
    features: List[List[float]],
    labels: List[int],
    train_ratio: float,
    seed: int,
) -> Tuple[List[List[float]], List[List[float]], List[int], List[int]]:
    if not 0.0 < train_ratio < 1.0:
        raise ValueError("train_ratio must be between 0 and 1")
    rand = rng(seed)
    indices = list(range(len(features)))
    rand.shuffle(indices)
    split = int(len(features) * train_ratio)
    train_idx, test_idx = indices[:split], indices[split:]
    x_train = [features[idx] for idx in train_idx]
    x_test = [features[idx] for idx in test_idx]
    y_train = [labels[idx] for idx in train_idx]
    y_test = [labels[idx] for idx in test_idx]
    return x_train, x_test, y_train, y_test
