from datetime import datetime

from webapp.db import db
from webapp.reddit_api.models import Post
from webapp.user.models import User

association_table = db.Table('association',
                             db.Column('query_id', db.Integer, db.ForeignKey('query.id')),
                             db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                             )


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    name = db.Column(db.String(50))
    value = db.Column(db.String(50))

    def __repr__(self):
        return '<{} = {}>'.format(self.name, self.value)


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('settings.id'))
    category = db.relationship("Settings", foreign_keys=[category_id])
    query_str = db.Column(db.String(50))
    age_id = db.Column(db.Integer, db.ForeignKey('settings.id'))
    age = db.relationship("Settings", foreign_keys=[age_id])
    status = db.Column(db.String(25))
    percent = db.Column(db.Integer)
    result_url = db.Column(db.String(12), index=True, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship("Post",
                            secondary=association_table,
                            backref="queries",
                            cascade="all",
                            passive_deletes=True
                            )

    def __repr__(self):
        return '<Запрос: {}>'.format(self.query_str)
