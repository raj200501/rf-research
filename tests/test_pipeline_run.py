import tempfile
import unittest
from pathlib import Path

from rf_research.config import RFConfig
from rf_research.pipeline import run_pipeline


class PipelineRunTests(unittest.TestCase):
    def _config_for(self, tmp_path: Path) -> RFConfig:
        base = RFConfig(samples=64, features=4, classes=2)
        return base.__class__(
            **{
                **base.__dict__,
                "data_path": tmp_path / "radio_frequencies.csv",
                "processed_path": tmp_path / "processed_radio_frequencies.csv",
                "model_path": tmp_path / "rfml_model.json",
                "report_path": tmp_path / "evaluation_report.json",
                "collection_path": tmp_path / "rf_collection.json",
                "analysis_path": tmp_path / "rf_analysis.json",
            }
        )

    def test_run_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = self._config_for(Path(tmp_dir))
            result = run_pipeline(config)
            self.assertTrue((Path(tmp_dir) / "rfml_model.json").exists())
            self.assertTrue((Path(tmp_dir) / "processed_radio_frequencies.csv").exists())
            self.assertTrue((Path(tmp_dir) / "signal_strength_summary.csv").exists())
            self.assertGreater(result.training_report["train_accuracy"], 0)


if __name__ == "__main__":
    unittest.main()
