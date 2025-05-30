FROM python:3.13-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip && pip install -r requirements.txt && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY app.py .
EXPOSE 5001
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]