from .models import URLScan
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import urlparse

from .features import extract_features, normalize_url, validate_url
from .ml_model import predict_url
from .threat_intel import apply_reputation_score, lookup_url_reputation

# Whitelist of known safe domains to reduce false positives
KNOWN_SAFE_DOMAINS = {
    'google.com', 'google.co', 'google.co.uk', 'google.ca', 'google.de', 'google.fr',
    'facebook.com', 'fb.com', 'facebook.co.uk',
    'amazon.com', 'amazon.co.uk', 'amazon.de', 'amazon.fr',
    'youtube.com', 'youtu.be',
    'twitter.com', 'x.com',
    'linkedin.com',
    'instagram.com',
    'microsoft.com', 'msn.com', 'outlook.com', 'hotmail.com',
    'apple.com', 'icloud.com',
    'netflix.com',
    'spotify.com',
    'reddit.com',
    'wikipedia.org', 'wikimedia.org',
    'github.com',
    'stackoverflow.com',
    'yahoo.com',
    'ebay.com',
    'paypal.com',
}


@api_view(['POST'])
def analyze_url(request):

    url = str(request.data.get('url') or '').strip()

    if not url:
        return Response(
            {"error": "A non-empty 'url' field is required."},
            status=400
        )

    # URL-only analysis never fetches the address. Reject malformed input before
    # extracting model features or storing it as a scan.
    url = normalize_url(url)
    if not validate_url(url):
        return Response({"error": "Provide a valid HTTP or HTTPS URL."}, status=400)

    # Extract features
    features = extract_features(url)

    # AI prediction
    prediction, local_probability = predict_url(features, url)
    reputation = lookup_url_reputation(url)
    probability, decision_source = apply_reputation_score(local_probability, reputation)
    
    # Check if URL is from a known safe domain
    parsed = urlparse(url)
    domain = parsed.hostname.lower() if parsed.hostname else ""
    
    # Check if domain is a subdomain of a known safe domain
    is_safe_domain = domain in KNOWN_SAFE_DOMAINS
    if not is_safe_domain:
        # Check if it's a subdomain of a known safe domain
        for safe_domain in KNOWN_SAFE_DOMAINS:
            if domain.endswith('.' + safe_domain):
                is_safe_domain = True
                break
    
    if is_safe_domain:
        probability = min(probability, 0.3)  # Cap probability for known safe domains
        decision_source = "local_ml+whitelist"
    
    # Add heuristic adjustments for clear phishing patterns
    path = parsed.path.lower() if parsed.path else ""
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    
    # Boost probability for suspicious subdomains with brand names
    if any(brand in hostname for brand in ["paypal", "apple", "google", "microsoft", "amazon", "facebook", "netflix", "instagram", "twitter", "linkedin", "ebay"]):
        if any(susp in hostname for susp in ["login", "secure", "account", "verify", "auth", "signin", "confirm", "wallet", "banking", "support"]):
            if domain not in KNOWN_SAFE_DOMAINS:
                probability = max(probability, 0.85)
                decision_source = "local_ml+heuristic"
    
    # Boost for generic suspicious domains with login-related paths
    if domain not in KNOWN_SAFE_DOMAINS:
        if any(term in path for term in ["login", "signin", "auth", "account", "verify", "secure", "confirm", "wallet", "banking"]):
            if any(susp in hostname for susp in ["secure", "account", "verify", "auth", "signin", "confirm", "wallet", "banking", "support"]):
                # Only boost if it's clearly suspicious (has brand name or very generic domain)
                if any(brand in hostname for brand in ["paypal", "apple", "google", "microsoft", "amazon", "facebook", "netflix", "instagram", "twitter", "linkedin", "ebay"]):
                    probability = max(probability, 0.75)
                    decision_source = "local_ml+heuristic"
                elif any(tld in hostname for tld in [".xyz", ".top", ".icu", ".gq", ".ml", ".cf", ".ga", ".tk", ".work", ".country", ".click", ".biz"]):
                    probability = max(probability, 0.75)
                    decision_source = "local_ml+heuristic"
    
    # Boost for IP addresses
    if features.get("has_ip"):
        probability = max(probability, 0.9)
        decision_source = "local_ml+heuristic"
    
    # Boost for suspicious TLDs
    if features.get("suspicious_tld"):
        probability = max(probability, 0.7)
        decision_source = "local_ml+heuristic"
    
    # Boost for domains with suspicious keywords
    if any(susp in hostname for susp in ["login", "secure", "account", "verify", "auth", "signin", "confirm", "wallet", "banking", "support", "malicious", "phishing", "scam"]):
        if domain not in KNOWN_SAFE_DOMAINS:
            probability = max(probability, 0.65)
            decision_source = "local_ml+heuristic"
    
    prediction = int(probability >= 0.5)

    # Determine risk level - adjusted thresholds to reduce false positives
    if probability >= 0.8:
        risk_level = "HIGH RISK"
    elif probability >= 0.6:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "SAFE"

    # Save scan to database
    scan = URLScan.objects.create(
        url=url,
        prediction=int(prediction),
        risk_score=round(probability * 100, 2),
        risk_level=risk_level
    )

    # Return response
    return Response({
        "id": scan.id,
        "url": url,
        "prediction": int(prediction),
        "risk_score": round(probability * 100, 2),
        "risk_level": risk_level,
        "features": features,
        "decision_source": decision_source,
        "reputation": reputation,
        "scanned_at": scan.scanned_at
    })


@api_view(['GET'])
def scan_history(request):

    scans = URLScan.objects.all().order_by('-scanned_at')[:20]

    data = []

    for scan in scans:
        data.append({
            "id": scan.id,
            "url": scan.url,
            "prediction": scan.prediction,
            "risk_score": scan.risk_score,
            "risk_level": scan.risk_level,
            "scanned_at": scan.scanned_at
        })

    return Response(data)


@api_view(['DELETE'])
def clear_history(request):

    URLScan.objects.all().delete()

    return Response({
        "message": "Scan history cleared successfully."
    })
