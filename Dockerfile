FROM python:3.10-slim

# Install basic build deps required by some native wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt
COPY requirements-sdk.txt requirements-sdk.txt

# Install Python deps (SDK deps may compile native packages)
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt || true
RUN python -m pip install -r requirements-sdk.txt || true

# Copy application
COPY . /app

EXPOSE 8501

# Default command prints helpful note; docker-compose will override commands for services
CMD ["/bin/bash","-c","echo 'Use docker-compose to run the web and agent services' && tail -f /dev/null"]
