from webapp import create_app
from webapp.db import db
from webapp.analysis.models import Category, Age
from webapp.user.models import User

app = create_app()

with app.app_context():
    categories = [('Политика', 'politics'), ('Новости', 'news')]
    for name, url in categories:
        if not Category.query.filter_by(name=name).count():
            new_category = Category(name=name, url=url)
            db.session.add(new_category)
            print(f'Добавлена категория {name}')
    db.session.commit()

    ages = [('Час', 'hour'), ('День', 'day'), ('Неделя', 'week'), ('Месяц', 'month'), ('Год', 'year'), ('Все время', 'all')]
    for name, value in ages:
        if not Age.query.filter_by(name=name).count():
            new_age = Age(name=name, value=value)
            db.session.add(new_age)
            print(f'Добавлен возраст {name}')
    db.session.commit()

    users = [('admin', 'admin')]
    for username, password in users:
        if not User.query.filter_by(username=username).count():
            new_user = User(username=username, role='admin')
            new_user.set_password(password)
            db.session.add(new_user)
            print(f'Добавлен пользователь {username}')
    db.session.commit()

    print('БД заполнена начальными данными')
