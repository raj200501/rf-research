"""Backward-compatible RF ML model wrapper."""

from rf_research.model import SoftmaxModel, train_softmax


RFMLModel = SoftmaxModel


def train_model(train_loader, epochs=10):
    features = []
    labels = []
    for batch_features, batch_labels in train_loader:
        if hasattr(batch_features, "tolist"):
            batch_features = batch_features.tolist()
        if hasattr(batch_labels, "tolist"):
            batch_labels = batch_labels.tolist()
        features.extend(batch_features)
        labels.extend(batch_labels)
    model, _ = train_softmax(
        features,
        labels,
        learning_rate=0.05,
        epochs=epochs,
        batch_size=64,
        seed=42,
    )
    return model
