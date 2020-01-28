from flask import Blueprint, render_template, redirect, url_for

from webapp.admin.forms import DeleteAllForm
from webapp.config import ROW_PER_PAGE
from webapp.db import db
from webapp.user.decorators import admin_required
from webapp.analysis.models import Query, Settings
from webapp.reddit_api.models import Post, Comment

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def index():
    title = 'Панель управления'
    return render_template('admin/index.html', page_title=title)


@blueprint.route('/setting')
@admin_required
def settings():
    title = 'Панель управления'
    page = 'Настройки'
    settings_list = Settings.query.all()
    return render_template('admin/settings.html', page_title=title, page=page, list=settings_list)


@blueprint.route('/queries', methods=['GET', 'POST'])
@blueprint.route('/queries/<int:page>', methods=['GET', 'POST'])
@admin_required
def queries(page=1):
    title = 'Панель управления'
    name = 'Запросы'
    queries = Query.query.paginate(page, ROW_PER_PAGE, False)
    form = DeleteAllForm()
    return render_template('admin/queries.html', page_title=title, name=name, queries=queries, form=form)


@blueprint.route('/posts', methods=['GET', 'POST'])
@blueprint.route('/posts/<int:page>', methods=['GET', 'POST'])
@admin_required
def posts(page=1):
    title = 'Панель управления'
    name = 'Посты'
    posts = Post.query.paginate(page, ROW_PER_PAGE, False)
    form = DeleteAllForm()
    return render_template('admin/posts.html', page_title=title, name=name, list=posts, form=form)


@blueprint.route('/comments', methods=['GET', 'POST'])
@blueprint.route('/comments/<int:page>', methods=['GET', 'POST'])
@admin_required
def comments(page=1):
    title = 'Панель управления'
    name = 'Комментарии'
    comments = Comment.query.paginate(page, ROW_PER_PAGE, False)
    return render_template('admin/comments.html', page_title=title, name=name, list=comments)


@blueprint.route('/delete_all', methods=['POST'])
@admin_required
def delete_all():
    form = DeleteAllForm()
    if form.validate_on_submit():
        if form.table.data == 'Query':
            for q in db.session.query(Query):
                q.posts.clear()
            db.session.query(Query).delete()
            db.session.commit()
            return redirect(url_for('admin.queries'))
        if form.table.data == 'Post':
            for p in db.session.query(Post):
                p.queries.clear()
            db.session.query(Comment).delete()
            db.session.query(Post).delete()
            db.session.commit()
            return redirect(url_for('admin.posts'))
    return redirect(url_for('admin.index'))
