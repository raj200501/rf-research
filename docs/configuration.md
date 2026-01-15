# Configuration Reference

The project uses the `RFConfig` dataclass (`rf_research/config.py`) as the single source of truth for defaults. You can override fields by passing CLI flags or by instantiating your own config in Python.

## Path Settings

| Field | Default | Description |
| --- | --- | --- |
| `data_path` | `data/radio_frequencies.csv` | Synthetic RF dataset CSV. |
| `processed_path` | `outputs/processed_radio_frequencies.csv` | Spark-like filtered output. |
| `model_path` | `models/rfml_model.json` | Trained model artifact. |
| `report_path` | `outputs/evaluation_report.json` | Training/evaluation report. |
| `collection_path` | `outputs/rf_collection.json` | RF data collection output. |
| `analysis_path` | `outputs/rf_analysis.json` | RF analysis report. |

## Dataset Parameters

| Field | Default | Description |
| --- | --- | --- |
| `samples` | `512` | Total number of synthetic samples generated. |
| `features` | `6` | Number of feature columns. |
| `classes` | `4` | Number of classes in the dataset. |
| `train_ratio` | `0.8` | Fraction of samples used for training. |
| `seed` | `42` | Random seed used for deterministic generation. |

## Training Parameters

| Field | Default | Description |
| --- | --- | --- |
| `learning_rate` | `0.05` | Gradient descent learning rate. |
| `epochs` | `50` | Number of epochs. |
| `batch_size` | `64` | Batch size for training. |

## CLI Overrides

Most fields can be overridden by passing CLI flags:

```bash
python -m rf_research.cli train \
  --data /tmp/rf.csv \
  --model /tmp/model.json \
  --outputs /tmp/outputs
```

The example above updates the dataset, model output, and report locations. Other parameters (samples, features, etc.) can be overridden by creating a custom configuration in a Python script.

## Example: Custom Config Script

```python
from rf_research.config import RFConfig
from rf_research.training import train_and_save

config = RFConfig(samples=1024, features=8, classes=5)
report = train_and_save(config)
print(report)
```

## Notes on Determinism

The following values are seeded to ensure deterministic runs:

- Dataset generation (`seed`)
- Model initialization and training shuffling (`seed`)
- National security data collection (`seed`)

To change randomness, update the seed in your custom config.
