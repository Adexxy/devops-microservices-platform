# services/order-service/Dockerfile
FROM python:3.13-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5003
CMD ["flask", "run", "--host=0.0.0.0", "--port=5003"]