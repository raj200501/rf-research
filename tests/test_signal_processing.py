import unittest

from rf_research.signal_processing import (
    add_noise,
    compute_fft,
    extract_features,
    generate_sine_wave,
    normalize_signal,
    resample,
)


class SignalProcessingTests(unittest.TestCase):
    def test_generate_sine_wave(self):
        signal = generate_sine_wave(100.0, 1000.0, 1.0)
        self.assertEqual(len(signal.samples), 1000)

    def test_add_noise_and_normalize(self):
        signal = generate_sine_wave(50.0, 1000.0, 1.0)
        noisy = add_noise(signal, noise_power=0.01, seed=1)
        normalized = normalize_signal(noisy)
        self.assertLessEqual(max(abs(value) for value in normalized.samples), 1.0)

    def test_fft_outputs(self):
        signal = generate_sine_wave(200.0, 1000.0, 1.0)
        freqs, spectrum = compute_fft(signal)
        self.assertEqual(len(freqs), len(spectrum))

    def test_extract_features(self):
        signal = generate_sine_wave(80.0, 1000.0, 1.0)
        features = extract_features(signal, noise_power=0.05)
        self.assertGreater(features.rms, 0)
        self.assertGreater(features.peak, 0)

    def test_resample(self):
        signal = generate_sine_wave(60.0, 1000.0, 1.0)
        resampled = resample(signal, 500.0)
        self.assertEqual(len(resampled.samples), 500)
        self.assertEqual(resampled.sample_rate_hz, 500.0)


if __name__ == "__main__":
    unittest.main()
