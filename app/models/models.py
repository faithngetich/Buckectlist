from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Defines the users model"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    bucketlists = db.relationship('BucketList', backref="user",
                                  cascade="all,delete-orphan", lazy='dynamic')

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def verify_password(self, password_hash, password):
        # return check_password_hash(self.password_hash, password)
        return check_password_hash(password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    
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

class BucketList(db.Model, UserMixin):
    """ Defines the bucketlist model"""
    __tablename__ = "bucket_list"
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    # created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    items = db.relationship('Item', backref="bucket_list",
                            cascade="all,delete-orphan", lazy='select')
    created_by = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))


    def __repr__(self):
        """Represents the bucketlist object"""
        return '<Bucketlist {0} : {1}>'.format(self.bucketlist_id, self.name)
    
class Item(db.Model, UserMixin):
    """ Defines the bucketlist items model """
    __tablename__='item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey('bucket_list.bucketlist_id', ondelete='CASCADE'))


    def __repr__(self):
        """Represents the item object"""
        return '<Item {0} : {1}>'.format(self.item_id, self.item_name)