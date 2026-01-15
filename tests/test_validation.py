import unittest

from rf_research.validation import raise_if_invalid


class ValidationTests(unittest.TestCase):
    def test_validation_rejects_nan(self):
        features = [[1.0, float("nan")]]
        labels = [0]
        with self.assertRaises(ValueError):
            raise_if_invalid(features, labels)

    def test_validation_rejects_length_mismatch(self):
        features = [[1.0, 2.0]]
        labels = [0, 1]
        with self.assertRaises(ValueError):
            raise_if_invalid(features, labels)


if __name__ == "__main__":
    unittest.main()
