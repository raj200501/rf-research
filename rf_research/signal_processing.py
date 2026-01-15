"""Signal processing helpers for RF simulation."""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import List, Tuple

import random


@dataclass(frozen=True)
class Signal:
    samples: List[float]
    sample_rate_hz: float

    def duration_seconds(self) -> float:
        return len(self.samples) / self.sample_rate_hz


@dataclass(frozen=True)
class SignalFeatures:
    rms: float
    peak: float
    snr_db: float
    centroid_hz: float
    bandwidth_hz: float


def generate_sine_wave(
    frequency_hz: float, sample_rate_hz: float, duration_seconds: float, phase: float = 0.0
) -> Signal:
    count = int(duration_seconds * sample_rate_hz)
    samples = [
        math.sin(2 * math.pi * frequency_hz * (idx / sample_rate_hz) + phase)
        for idx in range(count)
    ]
    return Signal(samples=samples, sample_rate_hz=sample_rate_hz)


def add_noise(signal: Signal, noise_power: float, seed: int) -> Signal:
    rand = random.Random(seed)
    noise_std = math.sqrt(noise_power)
    noisy_samples = [sample + rand.gauss(0.0, noise_std) for sample in signal.samples]
    return Signal(samples=noisy_samples, sample_rate_hz=signal.sample_rate_hz)


def normalize_signal(signal: Signal) -> Signal:
    max_val = max(abs(value) for value in signal.samples) if signal.samples else 0.0
    if max_val == 0:
        return signal
    return Signal(samples=[value / max_val for value in signal.samples], sample_rate_hz=signal.sample_rate_hz)


def compute_rms(samples: List[float]) -> float:
    if not samples:
        return 0.0
    return math.sqrt(sum(value * value for value in samples) / len(samples))


def compute_peak(samples: List[float]) -> float:
    return max(abs(value) for value in samples) if samples else 0.0


def compute_fft(signal: Signal) -> Tuple[List[float], List[complex]]:
    n = len(signal.samples)
    freqs = [idx * signal.sample_rate_hz / n for idx in range(n // 2 + 1)]
    spectrum = []
    for k in range(n // 2 + 1):
        total = 0j
        for t, sample in enumerate(signal.samples):
            angle = -2j * math.pi * k * t / n
            total += sample * cmath.exp(angle)
        spectrum.append(total)
    return freqs, spectrum


def compute_snr_db(signal: Signal, noise_power: float) -> float:
    if noise_power == 0:
        return float("inf")
    signal_power = sum(value * value for value in signal.samples) / len(signal.samples)
    return 10 * math.log10(signal_power / noise_power)


def spectral_centroid(freqs: List[float], spectrum: List[complex]) -> float:
    magnitudes = [abs(value) for value in spectrum]
    total = sum(magnitudes)
    if total == 0:
        return 0.0
    return sum(freq * magnitude for freq, magnitude in zip(freqs, magnitudes)) / total


def spectral_bandwidth(freqs: List[float], spectrum: List[complex], centroid: float) -> float:
    magnitudes = [abs(value) for value in spectrum]
    total = sum(magnitudes)
    if total == 0:
        return 0.0
    variance = sum(((freq - centroid) ** 2) * magnitude for freq, magnitude in zip(freqs, magnitudes)) / total
    return math.sqrt(variance)


def extract_features(signal: Signal, noise_power: float) -> SignalFeatures:
    freqs, spectrum = compute_fft(signal)
    centroid = spectral_centroid(freqs, spectrum)
    bandwidth = spectral_bandwidth(freqs, spectrum, centroid)
    return SignalFeatures(
        rms=compute_rms(signal.samples),
        peak=compute_peak(signal.samples),
        snr_db=compute_snr_db(signal, noise_power),
        centroid_hz=centroid,
        bandwidth_hz=bandwidth,
    )


def window_hann(signal: Signal) -> Signal:
    n = len(signal.samples)
    windowed = [sample * (0.5 - 0.5 * math.cos(2 * math.pi * idx / (n - 1))) for idx, sample in enumerate(signal.samples)]
    return Signal(samples=windowed, sample_rate_hz=signal.sample_rate_hz)


def window_hamming(signal: Signal) -> Signal:
    n = len(signal.samples)
    windowed = [sample * (0.54 - 0.46 * math.cos(2 * math.pi * idx / (n - 1))) for idx, sample in enumerate(signal.samples)]
    return Signal(samples=windowed, sample_rate_hz=signal.sample_rate_hz)


def resample(signal: Signal, new_sample_rate_hz: float) -> Signal:
    if new_sample_rate_hz <= 0:
        raise ValueError("new_sample_rate_hz must be positive")
    duration = signal.duration_seconds()
    count = int(duration * new_sample_rate_hz)
    new_samples = []
    for idx in range(count):
        t = idx / new_sample_rate_hz
        old_index = t * signal.sample_rate_hz
        low = int(math.floor(old_index))
        high = min(low + 1, len(signal.samples) - 1)
        if low == high:
            new_samples.append(signal.samples[low])
        else:
            weight = old_index - low
            interpolated = (1 - weight) * signal.samples[low] + weight * signal.samples[high]
            new_samples.append(interpolated)
    return Signal(samples=new_samples, sample_rate_hz=new_sample_rate_hz)
