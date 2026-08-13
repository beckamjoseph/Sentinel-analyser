"""Small, portable model wrapper for URL-only risk classification.

The wrapper keeps the text vectorizer, lexical feature scaler, classifier and
probability calibrator together.  Keeping the URL itself in the model input is
important: a handful of hand-written counts cannot distinguish many phishing
domains from ordinary domains.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import hstack

from .features import extract_features, normalize_url


class URLRiskModel:
    """Combine character n-grams with stable lexical URL signals."""

    expects_url = True

    def __init__(self, vectorizer, scaler, classifier, calibrator, feature_names):
        self.vectorizer = vectorizer
        self.scaler = scaler
        self.classifier = classifier
        self.calibrator = calibrator
        self.feature_names = list(feature_names)
        self.classes_ = np.array([0, 1])

    def _matrix(self, urls):
        normalized = [normalize_url(url) for url in urls]
        text = self.vectorizer.transform(normalized)
        lexical = np.asarray(
            [[extract_features(url)[name] for name in self.feature_names] for url in normalized],
            dtype=np.float64,
        )
        return hstack((text, self.scaler.transform(lexical)), format="csr")

    def predict_proba(self, urls):
        scores = self.classifier.decision_function(self._matrix(urls)).reshape(-1, 1)
        return self.calibrator.predict_proba(scores)
