"""Minimal math helpers for list-based numerical processing."""

from __future__ import annotations

import math
from typing import Iterable, List, Sequence, Tuple


def mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def variance(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    mu = mean(values)
    return sum((value - mu) ** 2 for value in values) / len(values)


def std(values: Sequence[float]) -> float:
    return math.sqrt(variance(values))


def transpose(matrix: Sequence[Sequence[float]]) -> List[List[float]]:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


def dot(row: Sequence[float], column: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(row, column))


def argmax(values: Sequence[float]) -> int:
    if not values:
        raise ValueError("argmax requires non-empty sequence")
    max_index = 0
    max_value = values[0]
    for idx, value in enumerate(values[1:], start=1):
        if value > max_value:
            max_value = value
            max_index = idx
    return max_index


def zeros(rows: int, cols: int) -> List[List[float]]:
    return [[0.0 for _ in range(cols)] for _ in range(rows)]


def add_vectors(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [x + y for x, y in zip(a, b)]


def sub_vectors(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [x - y for x, y in zip(a, b)]


def scalar_multiply(values: Sequence[float], scalar: float) -> List[float]:
    return [scalar * value for value in values]


def matrix_add(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> List[List[float]]:
    return [add_vectors(row_a, row_b) for row_a, row_b in zip(a, b)]


def matrix_sub(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> List[List[float]]:
    return [sub_vectors(row_a, row_b) for row_a, row_b in zip(a, b)]


def matrix_scalar_multiply(matrix: Sequence[Sequence[float]], scalar: float) -> List[List[float]]:
    return [scalar_multiply(row, scalar) for row in matrix]


def normalize(values: Sequence[float]) -> List[float]:
    total = sum(values)
    if total == 0:
        return [0.0 for _ in values]
    return [value / total for value in values]
