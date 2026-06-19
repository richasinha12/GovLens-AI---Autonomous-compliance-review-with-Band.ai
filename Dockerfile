FROM python:3.10-slim

# Install basic build deps required by some native wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    python3-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt
COPY requirements-sdk.txt requirements-sdk.txt

# Install Python deps (SDK deps may compile native packages)
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt
RUN if [ -f requirements-sdk.txt ]; then python -m pip install -r requirements-sdk.txt; fi

# Copy application
COPY . /app

EXPOSE 8501

# Default command: run Streamlit using the PORT env var (Render sets $PORT)
# If PORT is not set, default to 8501 for local testing.
CMD ["/bin/bash","-c","streamlit run main.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
