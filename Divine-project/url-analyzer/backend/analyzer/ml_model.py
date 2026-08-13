"""Model loading and score generation for the URL analysis API."""

import os

import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)


def _expected_feature_names() -> list[str] | None:
    """Support both the legacy classifier and newly calibrated model artifacts."""
    names = getattr(model, "feature_names_in_", None)
    if names is None:
        names = getattr(getattr(model, "estimator", None), "feature_names_in_", None)
    return list(names) if names is not None else None


def predict_url(features: dict, url: str | None = None) -> tuple[int, float]:
    """Return a malicious verdict and its model probability.

    Reindexing prevents an accidental feature-order mismatch and lets an older
    deployed model continue serving while a newly trained artifact is prepared.
    """
    # Newer models use character patterns from the original URL as well as the
    # numeric signals.  The fallback retains compatibility with old artifacts.
    if getattr(model, "expects_url", False):
        if not url:
            raise ValueError("The URL text is required by this model.")
        probability = float(model.predict_proba([url])[0][1])
        return int(probability >= 0.5), probability

    feature_values = pd.DataFrame([features])
    expected_names = _expected_feature_names()
    if expected_names:
        feature_values = feature_values.reindex(columns=expected_names, fill_value=0)

    probability = float(model.predict_proba(feature_values)[0][1])
    prediction = int(probability >= 0.5)
    return prediction, probability
