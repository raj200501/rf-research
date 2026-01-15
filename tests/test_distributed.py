import tempfile
import unittest
from pathlib import Path

from rf_research.config import RFConfig
from rf_research.data import generate_synthetic_dataset, write_dataset_csv
from rf_research.distributed.spark_job import process_data
from rf_research.distributed.hadoop_job import aggregate_signal_strength


class DistributedTests(unittest.TestCase):
    def _config_for(self, tmp_path: Path) -> RFConfig:
        base = RFConfig(samples=40, features=3, classes=2)
        return base.__class__(
            **{
                **base.__dict__,
                "data_path": tmp_path / "radio_frequencies.csv",
                "processed_path": tmp_path / "processed_radio_frequencies.csv",
            }
        )

    def test_spark_job_filters_rows(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = self._config_for(Path(tmp_dir))
            dataset = generate_synthetic_dataset(config)
            write_dataset_csv(config.data_path, dataset)
            output = process_data(config)
            self.assertTrue(output.exists())

    def test_hadoop_job_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = self._config_for(Path(tmp_dir))
            dataset = generate_synthetic_dataset(config)
            write_dataset_csv(config.data_path, dataset)
            output = aggregate_signal_strength(config)
            self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
