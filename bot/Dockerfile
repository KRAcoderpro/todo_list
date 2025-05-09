FROM python:3.10-slim

WORKDIR /app
COPY . /app/bot

RUN pip install --no-cache-dir -r /app/bot/requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "/app/bot/main.py"]
