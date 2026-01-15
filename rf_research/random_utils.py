"""Deterministic random helpers."""

from __future__ import annotations

import random
from typing import List, Sequence


def rng(seed: int) -> random.Random:
    return random.Random(seed)


def uniform_matrix(rand: random.Random, rows: int, cols: int, low: float, high: float) -> List[List[float]]:
    return [[rand.uniform(low, high) for _ in range(cols)] for _ in range(rows)]


def normal_matrix(rand: random.Random, rows: int, cols: int, mean: float, std_dev: float) -> List[List[float]]:
    return [[rand.gauss(mean, std_dev) for _ in range(cols)] for _ in range(rows)]


def shuffle_in_place(rand: random.Random, items: List[int]) -> None:
    rand.shuffle(items)


def choice(rand: random.Random, items: Sequence[float]) -> float:
    return rand.choice(items)
