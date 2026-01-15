"""Synthetic RF dataset generation and CSV IO."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

from rf_research.config import RFConfig
from rf_research.random_utils import normal_matrix, rng, uniform_matrix
from rf_research.simulation import SimulationConfig, default_scenarios, simulate_dataset


@dataclass(frozen=True)
class Dataset:
    features: List[List[float]]
    labels: List[int]


def generate_synthetic_dataset(config: RFConfig) -> Dataset:
    """Generate a synthetic RF dataset with labeled classes."""
    rand = rng(config.seed)
    centers = uniform_matrix(rand, config.classes, config.features, -2.0, 2.0)
    samples_per_class = config.samples // config.classes
    features: List[List[float]] = []
    labels: List[int] = []
    for class_idx, center in enumerate(centers):
        noise = normal_matrix(rand, samples_per_class, config.features, 0.0, 0.6)
        for row in noise:
            features.append([value + offset for value, offset in zip(row, center)])
            labels.append(class_idx)
    indices = list(range(len(labels)))
    rand.shuffle(indices)
    shuffled_features = [features[idx] for idx in indices]
    shuffled_labels = [labels[idx] for idx in indices]
    return Dataset(features=shuffled_features, labels=shuffled_labels)


def generate_signal_dataset(config: RFConfig) -> Dataset:
    """Generate a dataset derived from simulated RF signals."""
    sim_config = SimulationConfig(sample_rate_hz=1e6, duration_seconds=0.001, seed=config.seed)
    scenarios = default_scenarios()
    samples_per_scenario = max(1, config.samples // len(scenarios))
    result = simulate_dataset(scenarios, sim_config, samples_per_scenario)
    return Dataset(features=result.features, labels=result.labels)


def write_dataset_csv(path: Path, dataset: Dataset) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not dataset.features:
        raise ValueError("Dataset is empty")
    header = [f"feature_{idx}" for idx in range(len(dataset.features[0]))] + [
        "label",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row, label in zip(dataset.features, dataset.labels):
            writer.writerow([f"{value:.5f}" for value in row] + [int(label)])


def read_dataset_csv(path: Path) -> Dataset:
    with path.open("r", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None or len(header) < 2:
            raise ValueError("CSV header is missing feature columns or label column")
        rows: List[List[float]] = []
        labels: List[int] = []
        for row in reader:
            if not row:
                continue
            *feature_values, label = row
            rows.append([float(value) for value in feature_values])
            labels.append(int(label))
    return Dataset(features=rows, labels=labels)


def load_or_generate_dataset(config: RFConfig, use_signal_sim: bool = False) -> Dataset:
    """Load the dataset from disk or generate and persist if missing."""
    if config.data_path.exists():
        return read_dataset_csv(config.data_path)
    dataset = generate_signal_dataset(config) if use_signal_sim else generate_synthetic_dataset(config)
    write_dataset_csv(config.data_path, dataset)
    return dataset


def summarize_dataset(dataset: Dataset) -> dict:
    """Return summary statistics for the dataset."""
    samples = len(dataset.features)
    features = len(dataset.features[0]) if dataset.features else 0
    classes = len(set(dataset.labels))
    means = []
    stds = []
    for col in zip(*dataset.features):
        mean = sum(col) / len(col)
        variance = sum((value - mean) ** 2 for value in col) / len(col)
        means.append(mean)
        stds.append(variance ** 0.5)
    return {
        "samples": samples,
        "features": features,
        "classes": classes,
        "feature_mean": means,
        "feature_std": stds,
    }
