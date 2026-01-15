# RF Research Toolkit

This repository is a self-contained, reproducible RF research toolkit that simulates the original AWS ML Research Fellow project in a **local-only** environment. It provides:

- Synthetic RF dataset generation
- Lightweight ML training/evaluation (pure Python softmax classifier)
- Local Spark-like and Hadoop-like processing
- Core OS C integration sample with secure hash operations and monitoring
- National security RF data collection + analysis simulation

All workflows run locally without AWS, Hadoop, or Spark installations.

## Repository Layout

- `rf_research/`: Python package with the core workflows
- `ml-models/`: Backward-compatible entrypoints for ML training and evaluation
- `distributed-systems/`: Local Spark/Hadoop-like entrypoints
- `core-os/`: C implementation for secure operations and monitoring
- `national-security/`: Local RF data collection and analysis entrypoints
- `scripts/`: Bootstrap, run, and verification commands
- `docs/`: Extended documentation
- `examples/`: Example snippets and configs

## Requirements

- Python 3.10+ with venv support
- GCC (for `core-os` build)

## Verified Quickstart

```bash
./scripts/run.sh
```

The command above will:

1. Create a virtual environment
2. Generate a synthetic RF dataset
3. Train and evaluate the ML model
4. Run Spark-like and Hadoop-like data processing
5. Collect and analyze RF data (local simulation)
6. Build and run the core OS demo

## Verified Verification

```bash
./scripts/verify.sh
```

This runs unit tests plus an integration smoke test and exits non-zero on any failure.

## Key Outputs

After running the quickstart or verification scripts, you should see:

- `data/radio_frequencies.csv`: Generated RF dataset
- `models/rfml_model.json`: Trained model artifact
- `outputs/processed_radio_frequencies.csv`: Spark-like processed data
- `outputs/signal_strength_summary.csv`: Hadoop-like aggregate summary
- `outputs/rf_collection.json`: RF data collection output
- `outputs/rf_analysis.json`: RF analysis output
- `outputs/evaluation_report.json`: Evaluation report

## Documentation & Examples

- Documentation: `docs/README.md`
- Examples: `examples/README.md`

## Troubleshooting

See `docs/troubleshooting.md` for help with common setup issues.
