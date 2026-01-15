import random


def simulate_rf_signals():
    rand = random.Random(123)
    frequencies = [1e6 + idx * (1e9 - 1e6) / 99 for idx in range(100)]
    signal_strengths = [rand.random() for _ in range(100)]
    return frequencies, signal_strengths


def analyze_rf_signals(frequencies, signal_strengths):
    mean_strength = sum(signal_strengths) / len(signal_strengths)
    variance = sum((value - mean_strength) ** 2 for value in signal_strengths) / len(signal_strengths)
    return mean_strength, variance ** 0.5


if __name__ == "__main__":
    frequencies, signal_strengths = simulate_rf_signals()
    mean_strength, std_strength = analyze_rf_signals(frequencies, signal_strengths)
    print(f"Mean Signal Strength: {mean_strength}")
    print(f"Standard Deviation of Signal Strength: {std_strength}")
