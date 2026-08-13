"""Train a calibrated URL phishing/malware model.

Run from ``url-analyzer``:
    venv\\Scripts\\python.exe ml-model\\train.py
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import average_precision_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from analyzer.features import extract_features, normalize_url  # noqa: E402
from analyzer.url_model import URLRiskModel  # noqa: E402

DATA_PATH = BASE_DIR / "dataset" / "malicious_phish.csv"
BACKEND_MODEL_PATH = BACKEND_DIR / "model.pkl"
LOCAL_MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"
METRICS_PATH = BACKEND_DIR / "model_metrics.json"
# 100k representative URLs fit and retrain comfortably on the laptops this
# project targets; callers may raise this through the environment if desired.
MAX_TRAINING_ROWS = int(os.getenv("URL_ANALYZER_MAX_TRAINING_ROWS", "50000"))
FEATURE_NAMES = list(extract_features("https://example.com").keys())


def domain_group(url: str) -> str:
    """Keep registered-domain families out of both train and test partitions."""
    try:
        hostname = urlparse(normalize_url(url)).hostname or ""
    except ValueError:
        return "[malformed-url]"
    parts = hostname.lower().split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else hostname.lower()


def lexical_matrix(urls: pd.Series) -> np.ndarray:
    return np.asarray(
        [[extract_features(url)[name] for name in FEATURE_NAMES] for url in urls], dtype=np.float64
    )


def main() -> None:
    raw = pd.read_csv(DATA_PATH, usecols=["url", "type"]).dropna()
    # Do not use historical defacement labels as present-day malicious labels.
    raw = raw[raw["type"].isin(["benign", "phishing", "malware"])].copy()
    raw["label"] = (raw["type"] != "benign").astype(int)
    raw = raw.drop_duplicates(subset="url").reset_index(drop=True)
    raw["group"] = raw["url"].map(domain_group)

    # A representative cap keeps retraining practical on an ordinary laptop.
    if MAX_TRAINING_ROWS and len(raw) > MAX_TRAINING_ROWS:
        raw = pd.concat([
            group.sample(min(len(group), max(1, MAX_TRAINING_ROWS * len(group) // len(raw))), random_state=42)
            for _, group in raw.groupby("label")
        ], ignore_index=True)

    outer = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(outer.split(raw, raw["label"], raw["group"]))
    train, test = raw.iloc[train_idx].reset_index(drop=True), raw.iloc[test_idx].reset_index(drop=True)
    # Reserve domain-disjoint data for calibration; the final test set remains untouched.
    inner = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=7)
    fit_idx, calibration_idx = next(inner.split(train, train["label"], train["group"]))
    fit, calibration = train.iloc[fit_idx], train.iloc[calibration_idx]

    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(3, 4), min_df=2, max_features=50000,
                                 sublinear_tf=True, dtype=np.float32)
    x_fit_text = vectorizer.fit_transform(fit["url"].map(normalize_url))
    scaler = StandardScaler()
    x_fit = hstack((x_fit_text, scaler.fit_transform(lexical_matrix(fit["url"]))), format="csr")
    classifier = SGDClassifier(loss="log_loss", alpha=3e-6, max_iter=5, tol=1e-3,
                               early_stopping=True, validation_fraction=0.1, n_iter_no_change=5,
                               class_weight="balanced", average=False, random_state=42)
    classifier.fit(x_fit, fit["label"])

    def decision_values(frame):
        text = vectorizer.transform(frame["url"].map(normalize_url))
        return classifier.decision_function(hstack((text, scaler.transform(lexical_matrix(frame["url"]))), format="csr"))

    calibrator = LogisticRegression(class_weight="balanced", random_state=42)
    calibrator.fit(decision_values(calibration).reshape(-1, 1), calibration["label"])
    model = URLRiskModel(vectorizer, scaler, classifier, calibrator, FEATURE_NAMES)

    probabilities = model.predict_proba(test["url"].tolist())[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "model": "calibrated character n-gram + lexical URL classifier",
        "positive_classes": ["phishing", "malware"],
        "excluded_class": "defacement (historical/noisy for present-day URL safety)",
        "holdout": "domain-separated GroupShuffleSplit (20%)",
        "rows": int(len(raw)), "train_rows": int(len(train)), "test_rows": int(len(test)),
        "roc_auc": round(float(roc_auc_score(test["label"], probabilities)), 4),
        "average_precision": round(float(average_precision_score(test["label"], probabilities)), 4),
        "confusion_matrix": confusion_matrix(test["label"], predictions).tolist(),
        "classification_report": classification_report(test["label"], predictions, output_dict=True, zero_division=0),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    joblib.dump(model, BACKEND_MODEL_PATH, compress=3)
    joblib.dump(model, LOCAL_MODEL_PATH, compress=3)

    confusion_path = BASE_DIR / "confusion_matrix.png"
    cm = np.array(metrics["confusion_matrix"])
    plt.figure(figsize=(6, 4.5))
    plt.imshow(cm, interpolation="nearest", cmap="Blues")
    plt.title("Confusion Matrix of the URL Classifier")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.xticks([0, 1], ["Benign", "Malicious"])
    plt.yticks([0, 1], ["Benign", "Malicious"])
    for row in range(cm.shape[0]):
        for col in range(cm.shape[1]):
            plt.text(col, row, int(cm[row, col]), ha="center", va="center", color="black")
    plt.tight_layout()
    plt.savefig(confusion_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(json.dumps(metrics, indent=2))
    print(f"Confusion matrix image saved to {confusion_path}")


if __name__ == "__main__":
    main()
