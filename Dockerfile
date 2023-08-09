FROM python:3.9-slim-buster
RUN adduser --disabled-password --gecos '' myuser
WORKDIR /app
USER root
COPY requirements.txt ./
RUN chown -R myuser:myuser /app
USER myuser
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
EXPOSE 5000
