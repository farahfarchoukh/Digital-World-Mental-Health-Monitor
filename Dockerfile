FROM python:3.11-slim

# Add a non‑root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser
WORKDIR /home/appuser

# Install dependencies (layered for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
ENV PYTHONPATH=/home/appuser/src

# Install Functions Framework (already in requirements) – default entrypoint
CMD ["functions-framework", "--target", "collect"]
