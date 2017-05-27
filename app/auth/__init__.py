from app.models import User
from flask_restful import Resource, reqparse
from sqlalchemy.orm.exc import NoResultFound
from flask import request, jsonify, make_response

def identity(payload):
    username = payload['identity']
    return User.query.filter_by(id = username).first()

def authenticate(username, password):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, location='json', help="Username Required")
    parser.add_argument('password', type=str, required=True, location='json', help="Password Required")
    args = parser.parse_args()
    username = args.get('username')
    password = args.get('password')
    user = User(username=username, password=password)

    try:
        check_user = User.query.filter_by(username=username).one()
        passwor_hash = check_user.password
        verify_password = user.verify_password(passwor_hash, password)
        print('Here>>>>>', verify_password)
        if(verify_password):
            return check_user;
        return None
    except NoResultFound:
        return None
            
