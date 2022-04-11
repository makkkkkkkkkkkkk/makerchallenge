from requests_cache import ExpirationTime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.String(25), nullable=False)
    exipration_date = db.Column(db.String(25), nullable=False)
    pinned = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(150), db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Posts('{self.title}', '{self.date_posted}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    rank = db.Column(db.String(150), default="user")
    banned = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=func.now())

# class Comment(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
#     username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)