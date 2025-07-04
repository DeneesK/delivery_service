# === Stage 1: build with Poetry ===
FROM python:3.12-slim AS builder

ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry export --only main --without-hashes --output requirements.txt


# === Stage 2: runtime ===
FROM python:3.12-slim

RUN apt-get update && apt-get install -y make gcc g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

