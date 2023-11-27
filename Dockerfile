FROM python:3.12.0
FROM ubuntu:latest

ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD federico/federico /app
COPY federico/requirements.txt .
RUN apt-get update && apt-get install -y python3-pip libpq-dev pkg-config libcairo2-dev
RUN pip3 install --no-cache-dir -r requirements.txt
COPY federico/federico .
EXPOSE 8000
CMD ["uwsgi", "app.ini"]
CMD ["python3", "federico/manage.py", "runserver"]