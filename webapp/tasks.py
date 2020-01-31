from webapp.reddit_api.reddit_api import submissions, post_output, get_posts
from text_analysis import get_score, analyze_db
from webapp.analysis.models import Query
from webapp.db import db
from webapp.config import CELERY_BROCKER_URL

from celery import Celery

celery = Celery('webapp', broker=CELERY_BROCKER_URL)


@celery.task
def start_analyse(new_query_id):
    new_query = Query.query.filter_by(id=new_query_id).first()
    new_query.status = 'Запрос обрабатывается'
    db.session.commit()
    posts = submissions(new_query.query_str, new_query.category.url, new_query.age.value)
    post_output(posts)
    new_query.status = 'Запрос анализируется'
    db.session.commit()
    score = get_score(posts)
    new_result = Result(positive=score['pos'], negative=score['neg'], neutral=score['neu'])
    db.session.add(new_result)
    db.session.commit()
    new_query.status = 'Завершен'
    db.session.commit()


@celery.task
def start_analyse2(new_query_id):
    new_query = Query.query.get(new_query_id)
    new_query.status = 'Запрос обрабатывается'
    db.session.commit()
    get_posts(new_query.id)
    new_query.status = 'Запрос анализируется'
    score = analyze_db(new_query_id)
    new_query.status = 'Завершен'
    db.session.commit()
