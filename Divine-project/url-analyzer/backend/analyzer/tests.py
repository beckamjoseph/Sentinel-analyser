from django.test import SimpleTestCase

from .features import extract_features, normalize_url, validate_url


class URLFeatureTests(SimpleTestCase):
    def test_normalizes_a_scheme_less_url(self):
        self.assertEqual(normalize_url("example.com/login"), "http://example.com/login")

    def test_detects_a_real_ip_address_but_not_an_invalid_one(self):
        self.assertEqual(extract_features("http://192.168.1.10/login")["has_ip"], 1)
        self.assertEqual(extract_features("http://999.999.999.999/login")["has_ip"], 0)

    def test_exposes_new_lexical_signals(self):
        features = extract_features("https://xn--paypa1-abc.top//login?next=free%20bonus")
        self.assertEqual(features["has_punycode"], 1)
        self.assertEqual(features["suspicious_tld"], 1)
        self.assertEqual(features["double_slash_in_path"], 1)
        self.assertGreater(features["suspicious_keyword_count"], 0)

    def test_rejects_malformed_urls_before_feature_extraction(self):
        self.assertFalse(validate_url("not a url"))
        self.assertFalse(validate_url("https://"))
        self.assertTrue(validate_url("https://example.com/path"))


class ReputationTests(SimpleTestCase):
    def test_confirmed_harmless_reputation_reduces_a_local_false_positive(self):
        from .threat_intel import apply_reputation_score

        score, source = apply_reputation_score(0.94, {"status": "known", "harmless": 10})
        self.assertEqual(score, 0.15)
        self.assertEqual(source, "local_ml+reputation")

    def test_malicious_reputation_overrides_a_low_local_score(self):
        from .threat_intel import apply_reputation_score

        score, _ = apply_reputation_score(0.10, {"status": "known", "malicious": 1})
        self.assertEqual(score, 0.95)
