import tempfile
import unittest
from pathlib import Path

from rf_research.config import RFConfig
from rf_research.data import (
    generate_synthetic_dataset,
    generate_signal_dataset,
    write_dataset_csv,
    read_dataset_csv,
    summarize_dataset,
)


class DataTests(unittest.TestCase):
    def test_generate_synthetic_dataset_shape(self):
        config = RFConfig(samples=128, features=5, classes=4)
        dataset = generate_synthetic_dataset(config)
        self.assertEqual(len(dataset.features), 128)
        self.assertEqual(len(dataset.features[0]), 5)
        self.assertEqual(len(dataset.labels), 128)
        self.assertEqual(set(dataset.labels), {0, 1, 2, 3})

    def test_csv_roundtrip(self):
        config = RFConfig(samples=32, features=3, classes=2)
        dataset = generate_synthetic_dataset(config)
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "rf.csv"
            write_dataset_csv(path, dataset)
            loaded = read_dataset_csv(path)
            self.assertEqual(len(loaded.features), len(dataset.features))
            self.assertEqual(loaded.labels, dataset.labels)

    def test_generate_signal_dataset(self):
        config = RFConfig(samples=32, features=7, classes=4)
        dataset = generate_signal_dataset(config)
        self.assertEqual(len(dataset.features), len(dataset.labels))

    def test_summarize_dataset(self):
        config = RFConfig(samples=64, features=4, classes=2)
        dataset = generate_synthetic_dataset(config)
        summary = summarize_dataset(dataset)
        self.assertEqual(summary["samples"], 64)
        self.assertEqual(summary["features"], 4)
        self.assertEqual(summary["classes"], 2)


if __name__ == "__main__":
    unittest.main()
