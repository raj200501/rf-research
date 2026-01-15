# Examples

This directory contains small examples for using the RF Research Toolkit.

## Example 1: Custom Training Script

```python
from rf_research.config import RFConfig
from rf_research.training import train_and_save

config = RFConfig(samples=256, features=6, classes=3, epochs=25)
report = train_and_save(config)
print(report)
```

## Example 2: Full Pipeline Run

```bash
python -m rf_research.cli pipeline
```

This command will:

- Generate a dataset if missing
- Train a model
- Evaluate the model
- Produce Spark-like and Hadoop-like outputs
- Run the national security collection + analysis simulation

## Example 3: Signal Processing

```python
from rf_research.signal_processing import (
    generate_sine_wave,
    add_noise,
    normalize_signal,
    extract_features,
)

signal = generate_sine_wave(25e6, 1e9, 1e-6)
noisy = add_noise(signal, noise_power=0.05, seed=7)
normalized = normalize_signal(noisy)
features = extract_features(normalized, noise_power=0.05)
print(features)
```

## Example 4: Custom Simulation Dataset

```python
from rf_research.simulation import SimulationConfig, default_scenarios, simulate_dataset

scenarios = default_scenarios()
config = SimulationConfig(sample_rate_hz=1e6, duration_seconds=0.001, seed=123)
result = simulate_dataset(scenarios, config, samples_per_scenario=5)
print(result.features.shape)
```

## Example 5: Local Distributed Processing

```bash
python -m rf_research.cli spark
python -m rf_research.cli hadoop
```
