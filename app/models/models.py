from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import datetime
datetime.utcnow()
from sqlalchemy.orm import relationship, sessionmaker
import jwt

from app.config import config


class User(db.Model, UserMixin):
    """Defines the users model"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    # bucketlists = db.relationship('Bucketlist', backref="user",
    #                               cascade="all,delete-orphan", lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def encode_auth_token(self, id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': id
            }
            return jwt.encode(
                payload,
                config['SECRET'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the token
        :param token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(token, config['SECRET'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "< user: {}>".format(self.username)

class Bucketlist(db.Model, UserMixin):
    """ Defines the bucketlist model"""
    __tablename__ = "bucketlist"
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
    items = db.relationship('Item', backref="bucketlist",
                            cascade="all,delete-orphan", lazy='select')

    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __repr__(self):
        """Represents the bucketlist object"""
        return '<Bucketlist {0} : {1}>'.format(self.bucketlist_id, self.name)

class Item(db.Model, UserMixin):
    """ Defines the bucketlist items model """
    __tablename__='item'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    bucketlist_id = db.Column(db.ForeignKey('bucketlist.bucketlist_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey('bucketlist.bucketlist_id', ondelete='CASCADE'))


    def __repr__(self):
        """Represents the item object"""
        return '<Item {0} : {1}>'.format(self.item_id, self.name)