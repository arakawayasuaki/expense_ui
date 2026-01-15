FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        poppler-utils \
        tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY a2ui-extension /app/a2ui-extension
COPY agent /app/agent
COPY agent/pyproject.container.toml /app/agent/pyproject.toml

WORKDIR /app/agent
RUN pip install --no-cache-dir .

EXPOSE 10002
CMD ["python", "/app/agent/__main__.py", "--host", "0.0.0.0", "--port", "10002"]
