"""
tests/test_app.py - PyTest test suite for the Flask application.

Covers:
  - GET /health                        → 200 {"status": "ok"}
  - GET /add?a=1&b=2                   → 200 {"result": 3}
  - GET /add?a=-5&b=10                 → 200 {"result": 5}  (negatives)
  - GET /add?a=foo&b=2                 → 400 (non-integer a)
  - GET /add?a=1&b=bar                 → 400 (non-integer b)
  - GET /add?a=1.5&b=2                 → 400 (float is not int)
  - GET /add                           → 400 (missing params)
  - GET /add?a=1                       → 400 (missing b)
"""

import pytest
from app.main import app


@pytest.fixture
def client():
    """Create a Flask test client with testing mode enabled."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ──────────────────────────────── /health ────────────────────────────────── #

class TestHealth:
    def test_health_status_code(self, client):
        """Health endpoint must return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_body(self, client):
        """Health endpoint must return {"status": "ok"}."""
        response = client.get("/health")
        data = response.get_json()
        assert data == {"status": "ok"}


# ──────────────────────────────── /add (valid) ───────────────────────────── #

class TestAddValid:
    def test_add_positive_integers(self, client):
        """1 + 2 should equal 3."""
        response = client.get("/add?a=1&b=2")
        assert response.status_code == 200
        assert response.get_json() == {"result": 3}

    def test_add_negative_integers(self, client):
        """-5 + 10 should equal 5."""
        response = client.get("/add?a=-5&b=10")
        assert response.status_code == 200
        assert response.get_json() == {"result": 5}

    def test_add_zeros(self, client):
        """0 + 0 should equal 0."""
        response = client.get("/add?a=0&b=0")
        assert response.status_code == 200
        assert response.get_json() == {"result": 0}

    def test_add_large_numbers(self, client):
        """Large integers should still compute correctly."""
        response = client.get("/add?a=1000000&b=9000000")
        assert response.status_code == 200
        assert response.get_json() == {"result": 10000000}


# ──────────────────────────────── /add (invalid) ─────────────────────────── #

class TestAddInvalid:
    def test_non_integer_a(self, client):
        """Non-integer 'a' must return 400."""
        response = client.get("/add?a=foo&b=2")
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_non_integer_b(self, client):
        """Non-integer 'b' must return 400."""
        response = client.get("/add?a=1&b=bar")
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_float_rejected(self, client):
        """Float strings must return 400 (only strict integers accepted)."""
        response = client.get("/add?a=1.5&b=2")
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_missing_both_params(self, client):
        """Missing both params must return 400."""
        response = client.get("/add")
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_missing_b(self, client):
        """Missing 'b' must return 400."""
        response = client.get("/add?a=1")
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_missing_a(self, client):
        """Missing 'a' must return 400."""
        response = client.get("/add?b=2")
        assert response.status_code == 400
        assert "error" in response.get_json()
