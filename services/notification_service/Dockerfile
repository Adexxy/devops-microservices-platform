# services/notification-service/Dockerfile
FROM python:3.9-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5004
CMD ["flask", "run", "--host=0.0.0.0", "--port=5004"]