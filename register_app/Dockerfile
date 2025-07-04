# === Stage 1: build with Poetry ===
FROM python:3.12-slim AS builder

RUN pip install "poetry==1.8.2"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry export --without-hashes --only register_app --output requirements.txt


# === Stage 2: runtime ===
FROM python:3.12-slim

RUN apt-get update && apt-get install -y make gcc g++ gettext && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app


COPY --from=builder /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY register_app/ . 

