import unittest

from rf_research.metrics import classification_report, confusion_matrix, format_report


class MetricsTests(unittest.TestCase):
    def test_confusion_matrix(self):
        labels = [0, 1, 1, 0]
        preds = [0, 1, 0, 0]
        matrix = confusion_matrix(labels, preds, 2)
        self.assertEqual(len(matrix), 2)
        self.assertEqual(matrix[0][0], 2)

    def test_classification_report(self):
        labels = [0, 1, 1, 0]
        preds = [0, 1, 0, 0]
        report = classification_report(labels, preds)
        self.assertGreater(report.accuracy, 0)
        lines = format_report(report)
        self.assertTrue(lines[0].startswith("class"))


if __name__ == "__main__":
    unittest.main()
