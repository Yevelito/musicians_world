from datetime import datetime
from hashlib import md5
from time import time

import jwt
from flask import render_template, current_app
from flask_login import UserMixin
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login, app
from app.email import send_email

from app.search import add_to_index, remove_from_index, query_index

from sqlalchemy import text


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids = []
        query = text(f"SELECT id FROM {cls.Album} WHERE MATCH ('title') AGAINST (:expression IN BOOLEAN MODE)")
        query = query.bindparams(expression=expression)
        result = db.engine.execute(query)

        for row in result:
            ids.append(row[0])

        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))

        total = len(ids)
        query = cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id))
        paginated_query = query.paginate(page, per_page, False)

        return paginated_query.items, total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)



followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    albums = db.relationship('Album', backref='artist_name', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_albums(self):
        followed = Album.query.join(followers, (followers.c.followed_id == Album.artist_id)).filter(
            followers.c.follower_id == self.id)
        own = Album.query.filter_by(artist_id=self.id)
        return followed.union(own).order_by(desc(Album.year))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def send_password_reset_email(user):
        token = user.get_reset_password_token()
        send_email('[Microblog] Reset Your Password',
                   sender=current_app.config['ADMINS'][0],
                   recipients=[user.email],
                   text_body=render_template('email/reset_password.txt',
                                             user=user, token=token),
                   html_body=render_template('email/reset_password.html',
                                             user=user, token=token))

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Album(db.Model):
    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    year = db.Column(db.Integer)
    link = db.Column(db.String(500))
    songs_count = db.Column(db.Integer)
    songs = db.relationship('Song', backref='album', lazy='dynamic')
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Album {}({})>'.format(self.title, self.year)



    @staticmethod
    def search(query, page, per_page):
        search_results = Album.query.filter(Album.title.like(f'%{query}%')).paginate(page, per_page, False)

        albums = search_results.items
        total = search_results.total

        return albums, total


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    link = db.Column(db.String(500))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

    def __repr__(self):
        return '<Song {}>'.format(self.title)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
