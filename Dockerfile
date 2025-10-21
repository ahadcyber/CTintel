# Multi-stage Docker build for CTI Dashboard
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 ctiuser && \
    mkdir -p /app/logs && \
    chown -R ctiuser:ctiuser /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/ctiuser/.local

# Copy application files
COPY --chown=ctiuser:ctiuser . .

# Switch to non-root user
USER ctiuser

# Set Python path
ENV PATH=/home/ctiuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')"

# Run with Gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "web.app_enhanced:app"]
