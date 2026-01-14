# Architecture Overview

This project is organized into four primary domains that map to the original research focus, but implemented to run locally with deterministic outputs.

## 1. Machine Learning Workflow (`rf_research` + `ml-models`)

- **Data generation**: `rf_research.data.generate_synthetic_dataset` creates a deterministic synthetic dataset using a fixed seed.
- **Preprocessing**: `rf_research.preprocessing.StandardScaler` normalizes the dataset.
- **Model**: `rf_research.model.SoftmaxModel` implements a multi-class softmax classifier with NumPy-only training.
- **Training**: `rf_research.training.train_and_save` orchestrates dataset loading, preprocessing, and model training.
- **Evaluation**: `rf_research.evaluation.evaluate_model` loads the saved model and evaluates accuracy on the test split.

## 2. Distributed Systems Simulation (`rf_research.distributed` + `distributed-systems`)

To avoid heavy dependencies, Spark and Hadoop are simulated using pure Python:

- `rf_research.distributed.spark_job.process_data` filters the dataset by `feature_0 > 0` and writes the output CSV.
- `rf_research.distributed.hadoop_job.aggregate_signal_strength` computes per-label averages and writes a summary CSV.

## 3. Core OS Integration (`core-os`)

The C subsystem demonstrates low-level integration:

- `core-os/ai_integration.c` performs secure hashing using a bundled SHA-256 implementation (`core-os/sha256.c`).
- Monitoring is bounded by an iteration count for deterministic testing.

## 4. National Security Simulation (`rf_research.national_security`)

- `rf_research.national_security.collection` simulates RF data collection and writes JSON locally.
- `rf_research.national_security.analysis` computes summary statistics from the collection.

## Verification Strategy

- Unit tests validate each component in isolation.
- `scripts/verify.sh` runs the full pipeline and a smoke test that validates all expected artifacts.
