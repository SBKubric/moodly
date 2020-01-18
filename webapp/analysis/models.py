from datetime import datetime

from webapp.db import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)
    url = db.Column(db.String(20))
    queries = db.relationship('Query', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Категория {}>'.format(self.name)


class Age(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=True)
    value = db.Column(db.String(10))
    queries = db.relationship('Query', backref='age', lazy='dynamic')

    def __repr__(self):
        return '<Возраст {}>'.format(self.name)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    neutral = db.Column(db.Integer)
    queries = db.relationship('Query', backref='result', lazy='dynamic')

    def __repr__(self):
        return '<Результат {}>'.format(self.id)


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    query_str = db.Column(db.String(50))
    age_id = db.Column(db.Integer, db.ForeignKey('age.id'))
    status = db.Column(db.String(20))
    result_url = db.Column(db.String(12), index=True, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))

    def __repr__(self):
        return '<Запрос: {}(категория {}, возраст {})>'.format(self.query_str, self.category.name, self.age.name)
