# ==============================================================================
# ASTRAXIS-AI Production Multi-Stage Dockerfile
# Autonomous Multi-Agent AI Red-Teaming & Defense Sandbox Infrastructure
# ==============================================================================

# Stage 1: Base Python Environment & Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Build wheels
RUN pip install --no-cache-dir --upgrade pip setuptools build && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels .

# Stage 2: Final Lightweight Security Sandbox Runtime Image
FROM python:3.11-slim AS final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:${PATH}"

# Install minimal runtime system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-built wheels from builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/src /app/src
COPY pyproject.toml README.md ./

# Install wheels into container python environment
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Expose Streamlit default port 8501
EXPOSE 8501

# Healthcheck endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Non-root unprivileged security user
RUN useradd -m -u 1000 astraxisuser && \
    chown -R astraxisuser:astraxisuser /app
USER astraxisuser

# Default Entrypoint: Launch Streamlit Cyber Dashboard
CMD ["python", "-m", "streamlit", "run", "src/astraxis/ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
