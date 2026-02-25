FROM python:3.11-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy launcher application
COPY PythoRNG.py .

# Create data directory for shared volume
RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1

CMD ["python", "PythoRNG.py"]
