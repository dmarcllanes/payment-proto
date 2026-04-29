# ── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Build-time deps only (gcc needed to compile asyncpg C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /build

COPY pyproject.toml .

# Install all packages into an isolated venv via uv
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python --no-cache \
        python-fasthtml \
        "uvicorn[standard]" \
        httpx \
        polars \
        asyncpg \
        pydantic \
        pydantic-settings \
        python-dotenv \
        python-multipart


# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Only the runtime Postgres lib — no compiler, no headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# Pull compiled packages from builder (no gcc in final image)
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY . .

# Point to the venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Non-root user
RUN useradd -m -u 1000 jade && chown -R jade:jade /app
USER jade

EXPOSE ${PORT:-7860}

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-7860}/health || exit 1

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 2"]
