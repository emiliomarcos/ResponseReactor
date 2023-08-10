FROM python:3.9-slim-bullseye
RUN apt-get update && \
    apt-get install -y --no-install-recommends g++ build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password --gecos '' myuser
WORKDIR /app
USER root
COPY requirements.txt ./
RUN chown -R myuser:myuser /app
USER myuser
ENV HNSWLIB_NO_NATIVE=1
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "127.0.0.1:5000", "app:app"]
EXPOSE 5000
