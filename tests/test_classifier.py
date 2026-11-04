"""Tests for python/emg_classifier.py (run with: pytest tests/)."""
import os
import sys

import numpy as np
import pytest

pytest.importorskip("sklearn")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

from emg_classifier import EMGClassifier  # noqa: E402


def _separable_data(n_per_class=50, n_features=8, seed=0):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for label in range(4):
        center = np.zeros(n_features)
        center[label] = 5.0
        X.append(center + rng.standard_normal((n_per_class, n_features)) * 0.3)
        y.append(np.full(n_per_class, label))
    return np.vstack(X), np.concatenate(y)


def test_untrained_classifier_refuses_to_predict():
    clf = EMGClassifier()
    with pytest.raises(ValueError):
        clf.predict(np.zeros((1, 8)))
    with pytest.raises(ValueError):
        clf.save_model("unused.pkl")


def test_train_predict_and_evaluate_on_separable_data():
    X, y = _separable_data()
    clf = EMGClassifier(max_depth=8)
    info = clf.train(X, y)
    assert info["n_samples"] == len(y)
    assert info["classes"] == 4
    X_test, y_test = _separable_data(seed=1)
    metrics = clf.evaluate(X_test, y_test)
    assert metrics["accuracy"] > 0.95


def test_confidence_is_a_probability():
    X, y = _separable_data()
    clf = EMGClassifier()
    clf.train(X, y)
    preds, conf = clf.get_confidence(X[:10])
    assert preds.shape == (10,)
    assert np.all((conf >= 0.0) & (conf <= 1.0))


def test_save_and_load_round_trip(tmp_path):
    X, y = _separable_data()
    clf = EMGClassifier()
    clf.train(X, y)
    path = tmp_path / "model.pkl"
    clf.save_model(str(path))
    loaded = EMGClassifier()
    loaded.load_model(str(path))
    assert np.array_equal(loaded.predict(X), clf.predict(X))
