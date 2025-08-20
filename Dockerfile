# Deploy on Google Cloud Run
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates tzdata && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

HEALTHCHECK CMD python -c "import socket as s;import os;exit(0)"

CMD ["python", "-m", "app.main"]
