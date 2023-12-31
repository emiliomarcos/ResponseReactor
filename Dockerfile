FROM python:3.9-slim-bookworm
RUN apt-get update && \
    apt-get install -y --no-install-recommends g++ build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password --gecos '' myuser
WORKDIR /app
USER root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R myuser:myuser /app
USER myuser
CMD ["gunicorn", "--log-file", "-", "-b", "0.0.0.0:5000", "app:app"]
EXPOSE 5000
