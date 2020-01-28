from datetime import datetime

from flask import Blueprint, flash, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
import random
import string

from text_analysis import count_scores
from webapp.analysis.forms import QueryForm
from webapp.analysis.models import Settings, Query
from webapp.db import db
from webapp.tasks import start_analyse2
from webapp.reddit_api.models import Post, Comment

blueprint = Blueprint('analysis', __name__)


def load_select_field():
    all_category = Settings.query.filter_by(title='category')
    category_list = [(_.id, _.name) for _ in all_category]
    all_age = Settings.query.filter_by(title='age')
    age_list = [(_.id, _.name) for _ in all_age]
    form = QueryForm()
    form.category.choices = category_list
    form.age.choices = age_list
    return form


def create_unique_url():
    url_count = True
    while url_count:
        url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        url_count = Query.query.filter_by(result_url=url).count()
    return url


def summ_score(score_list):
    pos, neg, neu = 0, 0, 0
    for score in score_list:
        if score > 0.05:
            pos += 1
        elif score < -0.05:
            neg += 1
        else:
            neu += 1
    summ = pos + neu + neg
    if summ:
        percent = {'pos_percent': int(pos / summ * 100),
                   'neu_percent': int(neu / summ * 100),
                   'neg_percent': int(neg / summ * 100)}
    else:
        percent = {'pos_percent': 0, 'neu_percent': 100, 'neg_percent': 0}
    percent.update({'pos': pos, 'neu': neu, 'neg': neg})
    return percent


@blueprint.route("/")
def index():
    title = 'Анализ текста'
    query_form = load_select_field()
    return render_template('analysis/index.html', page_title=title, form=query_form)


@blueprint.route('/start', methods=['POST'])
def start():
    form = load_select_field()

    if form.validate_on_submit():
        result_url = create_unique_url()
        status = 'Запрос принят'
        if current_user.is_authenticated:
            user_id = int(current_user.get_id())
        else:
            user_id = None
        new_query = Query(category_id=form.category.data, query_str=form.query.data,
                          age_id=form.age.data, status=status, percent=0, result_url=result_url, user=user_id)
        db.session.add(new_query)
        db.session.commit()
        start_analyse2.delay(new_query.id)
        return redirect(url_for('analysis.result', result_url=result_url))

    flash('Неправильные данные')
    return redirect(url_for('analysis.index'))


@blueprint.route("/result/<result_url>")
def result(result_url):
    result = Query.query.filter_by(result_url=result_url).first()
    if result:
        return render_template('analysis/result.html', result=result)

    title = 'Ошибка. Запрос не наден'
    return render_template('analysis/result.html', page_title=title, result=result)


@blueprint.route("/update", methods=['POST'])
def update():
    result_url = request.form['code']
    result = Query.query.filter_by(result_url=result_url).options(db.joinedload(Query.posts)).first()
    if result:
        if result.status == 'Завершен':
            result_posts = summ_score([x.score for x in result.posts])
            comments = []
            authors = {}
            for post in result.posts:
                for comment in post.comments:
                    comments.append(comment.score)
                    if comment.author in authors:
                        authors[comment.author] += 1
                    else:
                        authors[comment.author] = 1
            result_comments = summ_score(comments)
            authors = {key: authors[key] for key in sorted(authors, key=authors.get, reverse=True)}
            html = render_template('analysis/done.html', result_posts=result_posts,
                                   result_comments=result_comments,
                                   authors=authors)
            end = True
        else:
            time_end = (datetime.utcnow() - result.date) * (1 - result.percent / 100) * 1.1
            time_end = str(time_end).split('.')[0]
            html = render_template('analysis/waiting.html', result=result, time_end=time_end)
            end = False
        return jsonify({"html": html, 'end': end})
    return jsonify({'html': 'ERROR', 'end': True})
