# ── Stage: runtime ────────────────────────────────────────────────────────────
# python:3.12-slim keeps the image small (no build tools, no dev headers).
FROM python:3.12-slim

# ── OS hardening ──────────────────────────────────────────────────────────────
# Create a dedicated non-root user and group so the process never runs as root.
RUN groupadd --gid 1001 appgroup && \
    useradd  --uid 1001 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Dependency layer (cached independently of source code) ────────────────────
# Copy ONLY requirements.txt first. Docker caches this layer and only
# re-runs pip when requirements.txt actually changes — not on every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application source ────────────────────────────────────────────────────────
# Copy source after deps so code-only changes don't bust the pip cache layer.
COPY app/ ./app/

# ── Runtime user ──────────────────────────────────────────────────────────────
# Drop privileges before starting the process.
USER appuser

# ── Network ───────────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Entrypoint ────────────────────────────────────────────────────────────────
# Gunicorn: 2 workers, binds to all interfaces on port 8000.
# app.main:app  →  the `app` Flask object inside app/main.py
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "app.main:app"]
