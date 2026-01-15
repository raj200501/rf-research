# API Reference

This reference documents the most important public functions. It is intentionally lightweight and focuses on the functions used by scripts and tests.

## `rf_research.config`

### `RFConfig`

`RFConfig` is the central configuration object. It stores paths and numeric defaults for the pipeline.

Key usage patterns:

- Instantiate with defaults: `config = RFConfig()`
- Override fields: `RFConfig(samples=1024, features=8)`
- Use `.ensure_directories()` before writing outputs

## `rf_research.data`

### `generate_synthetic_dataset`

Generates a deterministic dataset from class centers. Useful for quick smoke tests.

### `generate_signal_dataset`

Uses the signal simulation pipeline to derive features from synthetic RF signals. This provides more realistic signal-derived features.

### `write_dataset_csv` / `read_dataset_csv`

Serialize a dataset to CSV or load it back.

### `load_or_generate_dataset`

Loads the dataset from disk if present, otherwise generates and writes a new dataset.

## `rf_research.preprocessing`

### `StandardScaler`

Fits the mean and standard deviation of the dataset and scales features to zero mean/unit variance.

### `train_test_split`

Deterministic train/test split based on a seed.

## `rf_research.model`

### `SoftmaxModel`

A small pure-Python softmax classifier. The `save` and `load` methods serialize to a JSON artifact.

### `train_softmax`

Trains the model using gradient descent. Returns the model and `TrainingMetrics` containing losses and training accuracy.

## `rf_research.metrics`

### `confusion_matrix`

Builds a square matrix of true vs predicted labels.

### `classification_report`

Computes precision, recall, f1-score, and support for each class.

### `format_report`

Renders a human-readable report for the CLI output.

## `rf_research.training`

### `train_and_save`

End-to-end training pipeline. It loads/generates data, scales it, trains the model, and writes an artifact.

### `save_training_report`

Serializes training reports to JSON and Markdown.

## `rf_research.evaluation`

### `evaluate_model`

Loads the trained model, evaluates accuracy, and computes a classification report.

### `save_evaluation_report`

Writes evaluation reports to JSON and Markdown.

## `rf_research.distributed`

### `spark_job.process_data`

Filters the dataset based on `feature_0` and writes a processed CSV.

### `hadoop_job.aggregate_signal_strength`

Aggregates signal strength per label and writes a summary CSV.

## `rf_research.national_security`

### `collection.collect_and_save`

Generates synthetic RF observations and writes them to JSON.

### `analysis.analyze_and_save`

Loads the collection JSON and writes summary statistics.

## `rf_research.signal_processing`

Provides utilities for signal simulation, FFT analysis, and feature extraction. See `docs/signal-processing.md` for usage examples.

## `rf_research.pipeline`

### `run_pipeline`

Runs the full workflow (train, evaluate, distributed processing, and national security simulation). Returns a `PipelineResult` with the key outputs.
