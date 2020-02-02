from datetime import timedelta
import os


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://moodly:sengei8selaM@localhost:3306/moodly'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get('SECRET_KEY') or 'sdJKFH^czv$^v(vdv*&knm,csLKFc8Fj9'

REMEMBER_COOKIE_DURATION = timedelta(days=5)

CELERY_BROCKER_URL = os.environ.get('CELERY_BROCKER_URL') or 'redis://localhost'
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost'

ROW_PER_PAGE = 100
