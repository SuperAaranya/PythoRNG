FROM python:3.11-slim

WORKDIR /app/launcher

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY PythoRNG.py ./
COPY ../Game/Game\ Making/PythoRNG/pythorng_data.json ./data/ 2>/dev/null || true

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

CMD ["python", "PythoRNG.py"]
