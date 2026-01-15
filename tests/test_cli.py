import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_cli_generate(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_path = Path(tmp_dir) / "rf.csv"
            cmd = ["python", "-m", "rf_research.cli", "generate", "--data", str(data_path)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            payload = json.loads(result.stdout)
            self.assertTrue(Path(payload["data_path"]).exists())

    def test_cli_train_evaluate(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = Path(tmp_dir) / "outputs"
            outputs.mkdir()
            model_path = Path(tmp_dir) / "model.json"
            data_path = Path(tmp_dir) / "rf.csv"
            subprocess.run(
                ["python", "-m", "rf_research.cli", "generate", "--data", str(data_path)],
                check=True,
            )
            subprocess.run(
                [
                    "python",
                    "-m",
                    "rf_research.cli",
                    "train",
                    "--data",
                    str(data_path),
                    "--model",
                    str(model_path),
                    "--outputs",
                    str(outputs),
                ],
                check=True,
            )
            subprocess.run(
                [
                    "python",
                    "-m",
                    "rf_research.cli",
                    "evaluate",
                    "--data",
                    str(data_path),
                    "--model",
                    str(model_path),
                    "--outputs",
                    str(outputs),
                ],
                check=True,
            )
            self.assertTrue(model_path.exists())
            self.assertTrue((outputs / "evaluation_report.json").exists())


if __name__ == "__main__":
    unittest.main()
