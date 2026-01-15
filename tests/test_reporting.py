import tempfile
import unittest
from pathlib import Path

from rf_research.reporting import summarize_losses, write_markdown_summary, write_json


class ReportingTests(unittest.TestCase):
    def test_summarize_losses(self):
        result = summarize_losses([1.0, 0.5, 0.25])
        self.assertGreater(result["loss_mean"], 0)
        self.assertEqual(result["loss_final"], 0.25)

    def test_write_reports(self):
        report = {"accuracy": 0.9, "samples": 10}
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = Path(tmp_dir) / "report.json"
            md_path = Path(tmp_dir) / "report.md"
            write_json(report, json_path)
            write_markdown_summary(report, md_path)
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())


if __name__ == "__main__":
    unittest.main()
