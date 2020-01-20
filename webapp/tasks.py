from reddit_api import submissions, post_output
from text_analysis import analyze, count_scores
from webapp.analysis.models import Query, Result
from webapp.db import db


from celery import Celery

celery = Celery('webapp', broker='redis://localhost')


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
    new_query.result_id = new_result.id
    db.session.commit()
