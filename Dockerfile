# Use Python 3.8 slim base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5003

# Create and set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m homebridge && \
    chown -R homebridge:homebridge /app
USER homebridge

# Expose port
EXPOSE 5003

# Run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 app:app 