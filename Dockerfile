FROM python:3.12.0

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip libpq-dev pkg-config libcairo2-dev
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000