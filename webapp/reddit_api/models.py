from webapp.db import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reddit_id = db.Column(db.String(50))
    body = db.Column(db.Text)
    url = db.Column(db.String(50))
    score = db.Column(db.Float)
    comments = db.relationship('Comment', backref='comments', lazy='dynamic', cascade='all,delete-orphan')

    def __repr__(self):
        return '{}'.format(self.reddit_id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reddit_id = db.Column(db.String(50))
    body = db.Column(db.Text)
    url = db.Column(db.String(50))
    author = db.Column(db.String(50))
    score = db.Column(db.Float)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Комментарий {}>'.format(self.reddit_id)
