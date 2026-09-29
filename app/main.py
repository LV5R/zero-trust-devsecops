"""
app/main.py - Minimal Flask application for zero-trust-devsecops project.
Exposes two endpoints:
  GET /health  → {"status": "ok"}
  GET /add     → {"result": a + b}  (requires integer query params a and b)
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    """Health-check endpoint. Always returns HTTP 200 with status ok."""
    return jsonify({"status": "ok"}), 200


@app.get("/add")
def add():
    """
    Returns the sum of query parameters `a` and `b`.

    Query params:
        a (int): First operand.
        b (int): Second operand.

    Returns:
        200 {"result": <int>}  on success.
        400 {"error": <str>}   when a or b are missing or non-integer.
    """
    raw_a = request.args.get("a")
    raw_b = request.args.get("b")

    if raw_a is None or raw_b is None:
        return jsonify({"error": "Both query parameters 'a' and 'b' are required."}), 400

    try:
        a = int(raw_a)
        b = int(raw_b)
    except ValueError:
        return jsonify({"error": "Parameters 'a' and 'b' must be valid integers."}), 400

    return jsonify({"result": a + b}), 200


if __name__ == "__main__":
    app.run(debug=True)
