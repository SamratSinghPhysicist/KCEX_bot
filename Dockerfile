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

# Default command: Run Vivek Yadav SMC Multi-Asset concurrent portfolio (TRUMP, ETH, BTC, DOGE) in LIVE mode at 15x leverage
CMD ["python", "run_engine.py", "--preset", "MULTI_ASSET_SMC", "--mode", "live", "--leverage", "15", "--volume-mode", "MARGIN_PCT", "--margin-pct", "10.0", "--non-interactive"]
