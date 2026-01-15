import unittest

from rf_research.simulation import SimulationConfig, default_scenarios, simulate_dataset


class SimulationTests(unittest.TestCase):
    def test_simulate_dataset(self):
        scenarios = default_scenarios()
        config = SimulationConfig(sample_rate_hz=1e6, duration_seconds=0.001, seed=1)
        result = simulate_dataset(scenarios, config, samples_per_scenario=3)
        self.assertEqual(len(result.features), len(scenarios) * 3)
        self.assertEqual(len(result.labels), len(result.features))


if __name__ == "__main__":
    unittest.main()
