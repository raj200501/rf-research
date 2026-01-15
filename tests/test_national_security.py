import tempfile
import unittest
from pathlib import Path

from rf_research.config import RFConfig
from rf_research.national_security.collection import collect_and_save
from rf_research.national_security.analysis import analyze_and_save


class NationalSecurityTests(unittest.TestCase):
    def _config_for(self, tmp_path: Path) -> RFConfig:
        base = RFConfig()
        return base.__class__(
            **{
                **base.__dict__,
                "collection_path": tmp_path / "rf_collection.json",
                "analysis_path": tmp_path / "rf_analysis.json",
            }
        )

    def test_collection_and_analysis(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = self._config_for(Path(tmp_dir))
            collection_path = collect_and_save(config)
            self.assertTrue(collection_path.exists())
            analysis_path = analyze_and_save(config)
            self.assertTrue(analysis_path.exists())


if __name__ == "__main__":
    unittest.main()
