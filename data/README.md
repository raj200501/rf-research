# RF Dataset Directory

The RF research workflows generate a synthetic dataset at runtime.

- `radio_frequencies.csv` is created automatically by `rf_research.data.generate_synthetic_dataset`.
- The generated dataset is deterministic (seeded) to ensure repeatable tests.

To reset the dataset, delete the CSV file and rerun the training or data-generation commands.
