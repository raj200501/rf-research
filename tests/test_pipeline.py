import tempfile
import unittest
from pathlib import Path

from rf_research.config import RFConfig
from rf_research.training import train_and_save, save_training_report
from rf_research.evaluation import evaluate_model, save_evaluation_report


class PipelineTests(unittest.TestCase):
    def _config_for(self, tmp_path: Path) -> RFConfig:
        base = RFConfig()
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

    def test_train_and_evaluate(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = self._config_for(Path(tmp_dir))
            train_report = train_and_save(config)
            save_training_report(train_report, config.report_path)
            self.assertTrue(config.model_path.exists())
            eval_report = evaluate_model(config)
            save_evaluation_report(eval_report, config.report_path)
            self.assertIn("accuracy", eval_report)
            self.assertGreater(eval_report["samples"], 0)


if __name__ == "__main__":
    unittest.main()
