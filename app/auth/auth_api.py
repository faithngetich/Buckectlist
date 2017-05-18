from flask import jsonify, make_response
from . import auth
import jwt

from app.models import User
from app.config import config

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user
    return False

@auth.verify_token
def authenticate(auth_token):
    # auth_token = request.headers.get('Authorization') or  request.headers.get('x-access-token')
    if auth_token:
        try:
            payload = jwt.decode(auth_token, config['SECRET'])
            user_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

        user = User.query.filter_by(id=payload).first()

        if user:
            return True
        return make_response(
            jsonify({
                'data': {
                    'message': 'Invalid token'
                }}), 401)
    return make_response(
        jsonify({
            'data': {
                'message': 'Authorization token missing, Not allowed to view this content'
            }}), 401)
