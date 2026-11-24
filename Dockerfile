FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV DATABASE_PATH=/app/data/incidents.db

EXPOSE 5000

CMD ["python", "-m", "app.main"]
