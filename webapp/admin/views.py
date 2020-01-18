from flask import Blueprint, render_template

from webapp.user.decorators import admin_required
from webapp.analysis.models import Query

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = 'Панель управления'
    queries_list = Query.query.all()
    return render_template('admin/index.html', page_title=title, queries_list=queries_list)
