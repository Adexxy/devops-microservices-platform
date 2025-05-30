# services/order-service/Dockerfile
FROM python:3.9-slim-bullseye
WORKDIR /app

# Upgrade system packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY app.py .
EXPOSE 5003
CMD ["flask", "run", "--host=0.0.0.0", "--port=5003"]