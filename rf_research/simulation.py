"""RF signal simulation pipeline used to enrich datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import math
import random

from rf_research.signal_processing import (
    Signal,
    add_noise,
    extract_features,
    generate_sine_wave,
    normalize_signal,
)


@dataclass(frozen=True)
class Scenario:
    label: int
    frequency_hz: float
    noise_power: float
    amplitude: float = 1.0


@dataclass(frozen=True)
class SimulationConfig:
    sample_rate_hz: float
    duration_seconds: float
    seed: int


@dataclass(frozen=True)
class SimulationResult:
    features: List[List[float]]
    labels: List[int]
    scenarios: List[Scenario]


def _build_signal(scenario: Scenario, config: SimulationConfig, phase: float) -> Signal:
    signal = generate_sine_wave(
        frequency_hz=scenario.frequency_hz,
        sample_rate_hz=config.sample_rate_hz,
        duration_seconds=config.duration_seconds,
        phase=phase,
    )
    scaled = Signal(
        samples=[sample * scenario.amplitude for sample in signal.samples],
        sample_rate_hz=signal.sample_rate_hz,
    )
    noisy = add_noise(scaled, noise_power=scenario.noise_power, seed=config.seed)
    return normalize_signal(noisy)


def _scenario_feature_vector(signal: Signal, scenario: Scenario) -> List[float]:
    features = extract_features(signal, scenario.noise_power)
    return [
        features.rms,
        features.peak,
        features.snr_db,
        features.centroid_hz,
        features.bandwidth_hz,
        scenario.frequency_hz,
        scenario.noise_power,
    ]


def default_scenarios() -> List[Scenario]:
    return [
        Scenario(label=0, frequency_hz=1e6, noise_power=0.01, amplitude=1.0),
        Scenario(label=1, frequency_hz=2e6, noise_power=0.05, amplitude=0.8),
        Scenario(label=2, frequency_hz=3e6, noise_power=0.1, amplitude=0.6),
        Scenario(label=3, frequency_hz=4e6, noise_power=0.2, amplitude=0.5),
    ]


def simulate_dataset(
    scenarios: List[Scenario],
    config: SimulationConfig,
    samples_per_scenario: int,
) -> SimulationResult:
    rand = random.Random(config.seed)
    feature_rows: List[List[float]] = []
    labels: List[int] = []

    for scenario in scenarios:
        for _ in range(samples_per_scenario):
            phase = rand.uniform(0, 2 * math.pi)
            signal = _build_signal(scenario, config, phase)
            feature_rows.append(_scenario_feature_vector(signal, scenario))
            labels.append(scenario.label)

    indices = list(range(len(labels)))
    rand.shuffle(indices)
    shuffled_features = [feature_rows[idx] for idx in indices]
    shuffled_labels = [labels[idx] for idx in indices]
    return SimulationResult(
        features=shuffled_features,
        labels=shuffled_labels,
        scenarios=scenarios,
    )
