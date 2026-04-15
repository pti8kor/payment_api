# Stage 1: Build stage — install dependencies
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye AS builder

ARG HTTP_PROXY=
ARG HTTPS_PROXY=
ARG NO_PROXY=localhost,127.0.0.1

WORKDIR /app

# Copy only dependency files first (layer caching)
COPY requirements.txt .

RUN HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY} \
    pip install --upgrade pip && \
    HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY} \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image — copy app code
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye AS final

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY payments_api/ ./payments_api/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "payments_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
