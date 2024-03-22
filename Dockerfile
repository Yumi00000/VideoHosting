FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install any additional system packages you may need
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    useradd -ms /bin/bash celeryuser && \
    chown -R celeryuser /app
USER celeryuser

COPY . /app/


CMD python manage.py runserver
