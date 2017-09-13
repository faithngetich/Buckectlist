import json
from flask_restful import Resource, reqparse
from flask.views import MethodView
from sqlalchemy import exc
from flask_jwt import JWT, jwt_required, current_identity
from flask import request, jsonify, make_response, abort
from app.models import db
from ..models import User



class UserAPI(MethodView):
    """User Registration Resource"""
    def post(self):
        # get the post data
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json', help="Username Required")
        parser.add_argument('password', type=str, required=True, location='json', help="Password Required")
        args = parser.parse_args()

        username = args.get('username');
        password = args.get('password');

        if username=="" or password=="":
            response = jsonify({
                'status': 'failed',
                'Error': 'Empty username or password',
                'message': 'please enter username or password.',
            })
            return make_response(response, 400) # 409 => duplicate resources
            
            
        user = User(username=username, password=password);
        user.hash_password()
        db.session.add(user)
        try:
            db.session.commit()
            response = jsonify({
                'status': 'success',
                'user': {'username': username},
                'message': 'User created successfully',
            })
            return make_response(response, 201)
        except exc.IntegrityError:
            response = jsonify({
                'status': 'failed',
                'Error': 'Duplicate Username',
                'message': 'User already exists. Please Log in.',
            })
            return make_response(response, 409) # 409 => duplicate resources
