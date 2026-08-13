"""Deterministic, network-free URL features shared by training and inference.

These signals describe a URL; they do not contact or open the supplied address.
"""

from __future__ import annotations

import ipaddress
import math
import re
from collections import Counter
from urllib.parse import quote, unquote, urlparse


SUSPICIOUS_KEYWORDS = {
    "account", "auth", "bank", "bonus", "confirm", "credential", "ebay", "free",
    "login", "password", "paypal", "secure", "signin", "update", "verify", "webscr",
}
SUSPICIOUS_TLDS = {".biz", ".cf", ".click", ".country", ".ga", ".gq", ".icu", ".info", ".ml", ".ru", ".tk", ".top", ".work", ".xyz"}
COMMON_TLDS = {".com", ".co", ".edu", ".gov", ".io", ".net", ".org"}


def normalize_url(url: str) -> str:
    """Return a parseable URL without attempting to fetch it."""
    value = str(url or "").strip().strip("'\"")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        value = f"http://{value}"
    return value


def validate_url(url: str) -> bool:
    """Return True for well-formed HTTP or HTTPS URLs before analysis begins."""
    candidate = str(url or "").strip()
    if not candidate:
        return False

    if len(candidate) > 2048:
        return False

    # Check for spaces in URL
    if ' ' in candidate:
        return False

    try:
        parsed = urlparse(candidate)
    except ValueError:
        return False

    if parsed.scheme not in {"http", "https"}:
        return False
    if not parsed.netloc:
        return False
    
    # Check if netloc contains a valid hostname (no spaces)
    if ' ' in parsed.netloc:
        return False
    
    # Basic hostname validation
    hostname = parsed.hostname
    if not hostname:
        return False
    
    # Check if hostname has valid basic structure
    # Allow letters, numbers, dots, hyphens, underscores, and punycode
    # Punycode domains start with "xn--"
    if hostname.startswith('xn--'):
        # For punycode, just check it doesn't have spaces
        if ' ' in hostname:
            return False
    else:
        # For regular hostnames, check valid characters
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_')
        hostname_chars = set(hostname)
        if not hostname_chars.issubset(valid_chars):
            return False

    return True


def _is_ip_address(hostname: str) -> int:
    try:
        ipaddress.ip_address(hostname.strip("[]"))
        return 1
    except ValueError:
        return 0


def _entropy(value: str) -> float:
    if not value:
        return 0.0
    frequencies = Counter(value)
    length = len(value)
    return round(-sum((count / length) * math.log2(count / length) for count in frequencies.values()), 4)


def _has_explicit_port(parsed) -> int:
    try:
        return int(parsed.port is not None)
    except ValueError:
        # A malformed port is itself not a usable URL; keep feature extraction
        # robust so the request can receive a controlled validation response.
        return 0


def extract_features(url: str) -> dict[str, float | int]:
    """Build stable lexical features for a URL classifier.

    Keep feature names stable: existing serialized models are reindexed against the
    names they were trained on in ``ml_model.predict_url``.
    """
    normalized_url = normalize_url(url)
    try:
        parsed = urlparse(normalized_url)
    except ValueError:
        parsed = urlparse(f"http://invalid.local/{quote(normalized_url, safe='')}")

    hostname = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    decoded_url = unquote(normalized_url).lower()
    host_parts = [part for part in hostname.split(".") if part]
    url_lower = normalized_url.lower()

    features: dict[str, float | int] = {
        # Original feature set: retained so the currently saved model still works.
        "url_length": len(normalized_url),
        "domain_length": len(hostname),
        "path_length": len(path),
        "dot_count": normalized_url.count("."),
        "hyphen_count": normalized_url.count("-"),
        "underscore_count": normalized_url.count("_"),
        "slash_count": normalized_url.count("/"),
        "question_count": normalized_url.count("?"),
        "equal_count": normalized_url.count("="),
        "ampersand_count": normalized_url.count("&"),
        "at_count": normalized_url.count("@"),
        "digit_count": sum(character.isdigit() for character in normalized_url),
        "uses_https": int(parsed.scheme.lower() == "https"),
        "has_ip": _is_ip_address(hostname),
        "suspicious_keyword_count": sum(keyword in decoded_url for keyword in SUSPICIOUS_KEYWORDS),
        "suspicious_tld": int(any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS)),
        "subdomain_count": max(len(host_parts) - 2, 0),
        "is_root_domain": int(len(host_parts) == 2 or (len(host_parts) == 3 and host_parts[0] == "www")),
        "is_common_tld": int(any(hostname.endswith(tld) for tld in COMMON_TLDS)),
        # Additional signals used after retraining the model.
        "hostname_digit_count": sum(character.isdigit() for character in hostname),
        "hostname_hyphen_count": hostname.count("-"),
        "query_length": len(query),
        "query_parameter_count": int(bool(query)) + query.count("&"),
        "percent_encoding_count": normalized_url.count("%"),
        "double_slash_in_path": int("//" in path),
        "has_explicit_port": _has_explicit_port(parsed) if hostname else 0,
        "has_punycode": int("xn--" in hostname),
        "has_fragment": int(bool(parsed.fragment)),
        "contains_redirect_term": int(any(term in decoded_url for term in ("redirect", "redirecturl", "returnurl", "next="))),
        "url_entropy": _entropy(normalized_url.lower()),
        "hostname_entropy": _entropy(hostname),
    }
    return features
