# Signal Processing Reference

The module `rf_research.signal_processing` contains helper utilities for generating and analyzing synthetic RF signals. These helpers are used in tests and can be extended for research experiments.

## Signal Generation

### `generate_sine_wave`

Creates a sine wave with the specified frequency, sample rate, duration, and phase.

```python
from rf_research.signal_processing import generate_sine_wave

signal = generate_sine_wave(
    frequency_hz=915e6,
    sample_rate_hz=5e9,
    duration_seconds=1e-6,
    phase=0.0,
)
```

### `add_noise`

Adds Gaussian noise to a signal with deterministic seeding.

```python
from rf_research.signal_processing import add_noise

noisy_signal = add_noise(signal, noise_power=0.01, seed=42)
```

### `normalize_signal`

Normalizes a signal so its peak magnitude is 1.0. Useful for comparing signal levels.

## FFT Utilities

### `compute_fft`

Computes the FFT and returns the frequency bins and spectrum.

### `spectral_centroid`

Calculates the center of mass of the spectrum.

### `spectral_bandwidth`

Computes the standard deviation of the spectrum around the centroid.

## Feature Extraction

### `extract_features`

Returns a `SignalFeatures` dataclass with:

- RMS
- Peak
- SNR (dB)
- Spectral centroid
- Spectral bandwidth

```python
from rf_research.signal_processing import extract_features

features = extract_features(noisy_signal, noise_power=0.01)
print(features)
```

## Windowing

Windowing reduces spectral leakage. The module provides:

- `window_hann`
- `window_hamming`

Each returns a new `Signal` with the window applied.

## Resampling

`resample` uses linear interpolation to convert a signal to a different sample rate.

```python
from rf_research.signal_processing import resample

resampled = resample(signal, new_sample_rate_hz=2.5e9)
```

## Example Workflow

```python
from rf_research.signal_processing import (
    generate_sine_wave,
    add_noise,
    normalize_signal,
    extract_features,
)

signal = generate_sine_wave(100e6, 1e9, 1e-6)
noisy = add_noise(signal, noise_power=0.05, seed=7)
normalized = normalize_signal(noisy)
features = extract_features(normalized, noise_power=0.05)

print(features.rms)
print(features.peak)
```

## Notes

- These utilities are intentionally lightweight to keep the repo easy to run.
- For high-fidelity RF processing, integrate a dedicated DSP library as needed.
