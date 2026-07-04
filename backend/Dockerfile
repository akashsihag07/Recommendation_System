FROM python:3.11-slim

WORKDIR /app

# install deps first so docker caches this layer when only my code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY data/ ./data/

EXPOSE 8000

# --host 0.0.0.0 is needed or the container only listens on localhost inside
# itself and nothing can reach it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
