"""Validation helpers for RF workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import math


@dataclass(frozen=True)
class ValidationIssue:
    message: str
    level: str


def validate_features(features: List[List[float]]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    if not isinstance(features, list):
        issues.append(ValidationIssue("Features must be a list", "error"))
        return issues
    if not features:
        issues.append(ValidationIssue("Dataset has no rows", "error"))
        return issues
    row_length = len(features[0])
    for row in features:
        if len(row) != row_length:
            issues.append(ValidationIssue("Inconsistent feature row lengths", "error"))
            break
        for value in row:
            if math.isnan(value):
                issues.append(ValidationIssue("Dataset contains NaN values", "error"))
                break
            if math.isinf(value):
                issues.append(ValidationIssue("Dataset contains infinite values", "error"))
                break
    return issues


def validate_labels(labels: List[int]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    if not isinstance(labels, list):
        issues.append(ValidationIssue("Labels must be a list", "error"))
        return issues
    if not labels:
        issues.append(ValidationIssue("Dataset has no labels", "error"))
    if min(labels) < 0:
        issues.append(ValidationIssue("Labels must be non-negative", "error"))
    return issues


def validate_dataset(features: List[List[float]], labels: List[int]) -> List[ValidationIssue]:
    issues = validate_features(features)
    issues.extend(validate_labels(labels))
    if len(features) != len(labels):
        issues.append(ValidationIssue("Features and labels length mismatch", "error"))
    return issues


def raise_if_invalid(features: List[List[float]], labels: List[int]) -> None:
    issues = validate_dataset(features, labels)
    errors = [issue for issue in issues if issue.level == "error"]
    if errors:
        messages = "; ".join(issue.message for issue in errors)
        raise ValueError(messages)
