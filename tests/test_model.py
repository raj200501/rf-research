import random
import unittest

from rf_research.model import train_softmax, evaluate_accuracy
from rf_research.preprocessing import StandardScaler


class ModelTests(unittest.TestCase):
    def test_train_softmax_improves_accuracy(self):
        rand = random.Random(0)
        features = [[rand.gauss(0.0, 1.0) for _ in range(4)] for _ in range(200)]
        labels = [1 if row[0] + row[1] > 0 else 0 for row in features]
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)

        model, metrics = train_softmax(
            scaled,
            labels,
            learning_rate=0.1,
            epochs=30,
            batch_size=32,
            seed=0,
        )
        accuracy = evaluate_accuracy(model, scaled, labels)
        self.assertGreaterEqual(metrics.accuracy, 0.75)
        self.assertGreaterEqual(accuracy, 0.75)


if __name__ == "__main__":
    unittest.main()
