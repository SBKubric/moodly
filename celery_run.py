from webapp.tasks import celery
from webapp import create_app, init_celery

app = create_app()

with app.app_context():
    init_celery(app, celery)
