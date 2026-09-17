FROM python:3.11-slim

# Prevent python from buffering stdout/stderr and writing pyc files
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install minimal base packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies first to cache build layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy codebase and trained ML models
COPY . .

# Create logs directory
RUN mkdir -p logs

# Default command: Run ML 1M Bot on TRUMP_USDT in LIVE mode at 10x leverage with 1 contract
CMD ["python", "run_engine.py", "--preset", "TRUMP_ML_RAPID_SCALPER", "--mode", "live", "--symbol", "TRUMP_USDT", "--leverage", "10", "--volume-mode", "CONTRACTS", "--volume-contracts", "1", "--non-interactive"]
