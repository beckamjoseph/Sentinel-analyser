"""Compatibility import for scripts run from the ``ml-model`` directory.

The production API and the training code deliberately use the same feature code.
"""

import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from analyzer.features import extract_features, normalize_url  # noqa: E402,F401
