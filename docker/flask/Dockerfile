FROM python:3.7.6-alpine

WORKDIR /moodly
COPY . .
RUN pip install -r requirements.txt && chmod +x run.sh

ENV FLASK_APP webapp