"""Backward-compatible preprocessing utilities."""

from rf_research.data import load_or_generate_dataset
from rf_research.preprocessing import StandardScaler
from rf_research.config import RFConfig


def load_data(file_path=None):
    config = RFConfig()
    if file_path is not None:
        config = config.__class__(**{**config.__dict__, "data_path": file_path})
    dataset = load_or_generate_dataset(config)
    return dataset.features, dataset.labels


def preprocess_data(features):
    scaler = StandardScaler()
    return scaler.fit_transform(features)
