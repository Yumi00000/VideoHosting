FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    useradd -ms /bin/bash celeryuser && \
    chown -R celeryuser /app

USER celeryuser


COPY . /app/

CMD python manage.py runserver
