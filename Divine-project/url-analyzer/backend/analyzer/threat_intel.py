"""Optional reputation enrichment for higher-confidence URL decisions.

Set ``VIRUSTOTAL_API_KEY`` to enable it. This is intentionally opt-in because
URLs sent to a reputation provider may be sensitive.
"""

import base64
import os
from functools import lru_cache

import requests


API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "").strip()
API_URL = "https://www.virustotal.com/api/v3/urls/{}"


@lru_cache(maxsize=512)
def lookup_url_reputation(url: str) -> dict:
    """Return an external reputation summary, or a non-failing unavailable state."""
    if not API_KEY:
        return {"enabled": False, "status": "not_configured"}

    url_id = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    try:
        response = requests.get(
            API_URL.format(url_id), headers={"x-apikey": API_KEY}, timeout=5
        )
        if response.status_code == 404:
            return {"enabled": True, "status": "unknown"}
        response.raise_for_status()
        stats = response.json()["data"]["attributes"].get("last_analysis_stats", {})
        return {
            "enabled": True, "status": "known",
            "malicious": int(stats.get("malicious", 0)),
            "suspicious": int(stats.get("suspicious", 0)),
            "harmless": int(stats.get("harmless", 0)),
        }
    except (requests.RequestException, KeyError, TypeError, ValueError):
        # Threat intelligence should strengthen a result, never take the local
        # detector offline when the provider is unavailable or rate-limited.
        return {"enabled": True, "status": "unavailable"}


def apply_reputation_score(local_probability: float, reputation: dict) -> tuple[float, str]:
    """Combine local ML with confirmed multi-engine reputation when available."""
    if reputation.get("status") != "known":
        return local_probability, "local_ml"
    if reputation.get("malicious", 0) or reputation.get("suspicious", 0):
        return max(local_probability, 0.95), "local_ml+reputation"
    if reputation.get("harmless", 0) >= 5:
        return min(local_probability, 0.15), "local_ml+reputation"
    return local_probability, "local_ml+reputation"
