from flask import Blueprint, flash, render_template, redirect, url_for
import random
import string

from webapp.analysis.forms import QueryForm
from webapp.analysis.models import Category, Age, Query
from webapp.db import db
from webapp.tasks import start_analyse

blueprint = Blueprint('analysis', __name__)


def load_select_field():
    all_category = Category.query.all()
    category_list = [(_.id, _.name) for _ in all_category]
    all_age = Age.query.all()
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
        new_query = Query(category_id=form.category.data, query_str=form.query.data,
                          age_id=form.age.data, status=status, result_url=result_url)
        db.session.add(new_query)
        db.session.commit()
        start_analyse.delay(new_query.id)
        return redirect(url_for('analysis.result', result_url=result_url))

    flash('Неправильные данные')
    return redirect(url_for('analysis.index'))


@blueprint.route("/result/<result_url>")
def result(result_url):
    result = Query.query.filter_by(result_url=result_url).first()
    if result:
        return render_template('analysis/result.html', result=result)

    title = 'Ошибка. Запрос не наден'
    return render_template('analysis/result.html', page_title=title)
