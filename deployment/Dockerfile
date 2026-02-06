FROM python:3.11-slim

WORKDIR /app

# Copy requirements from config directory
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

LABEL org.opencontainers.image.source=https://github.com/SuperAaranya/PythoRNG
LABEL org.opencontainers.image.description="Pytho-RNG - A random number generator gaming application with Discord webhook integration"
