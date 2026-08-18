# Multi-stage build: dependencies resolve in the builder, only the package ships.
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install pytest coverage flake8
COPY src/ ./src/

FROM python:3.12-slim
LABEL org.opencontainers.image.title="wordcount" \
      org.opencontainers.image.description="Text statistics demo target for MiniCI"
WORKDIR /app
COPY --from=builder /build/src/ /app/src/
ENV PYTHONPATH=/app/src PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 appuser
USER appuser
ENTRYPOINT ["python", "-m", "wordcount.cli"]
CMD ["--help"]
