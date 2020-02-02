FROM python:3.7.6-alpine

WORKDIR /moodly
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY webapp webapp
COPY migrations migrations
COPY celery_run.py run.sh text_analysis.py create_first_data.py ./
RUN chmod +x run.sh

ENV FLASK_APP webapp