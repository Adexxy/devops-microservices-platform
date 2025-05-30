# services/product-service/Dockerfile
FROM python:3.9-slim-bookworm
WORKDIR /app
COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip && pip install -r requirements.txt && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY app.py .
EXPOSE 5002
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]