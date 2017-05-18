from flask import request, jsonify, make_response
from flask_restful import Resource

from app import db
from ..models import User
from ..auth import auth_api, auth

class UserAPI(Resource):
    # @auth.login_required
    def get(self, user_id):
        if isinstance(user_id, int):
            user = get_users(user_id)
        else:
            return make_response(
                jsonify({'data': {
                'Error': 'user_id should be an integer'
            }}), 400)

        if user:
            return make_response(
                jsonify({'data':{
                'id': user.id,
                'username': user.username,
                'email': user.email
            }}), 200)

        else:
            return make_response(
                jsonify({'data': {
                'Error': 'User not found'
            }}), 404)

    # @auth.login_required
    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return make_response(
                jsonify({'data': {
                'Error': 'User not found'
            }}), 404)
        try:
            user.username = request.form['username'] or user.username,
            user.email = request.form['email'] or user.email,
            user.password = request.form['password'] or user.password
            db.session.add(user)
            db.session.commit()
            return make_response(
                jsonify({'data': { 'user':{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'message': 'User updated successfully'}}), 204)

        except Exception as error:
            return make_response(
                jsonify({'data': {
                    'Error': str(error)
                }}), 400
            )

    # @auth.login_required
    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(
                jsonify({'data': {
                'Error': 'User not found'
            }}), 404)
        db.session.delete(user)
        db.session.commit()

        return make_response(
            jsonify({'data': {
                'message': user.username + 'deleted successfully'
            }}), 204)


class UsersList(Resource):
    # @auth.login_required
    def get(self):
        users = get_users(user_id=None)

        if users:
            return make_response(
                jsonify({'data': [{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                } for user in users]}), 200)

        else:
            return make_response(
                jsonify({'data': {
                    'Error': 'User not found'
                }}), 404)

    def post(self):
        user = User.query.filter_by(email=request.form['email']).first()
        if not user:
            try:
                user = User(
                    username=request.form['username'],
                    email=request.form['email'],
                    password=request.form['password']
                )

                db.session.add(user)
                db.session.commit()

            except Exception as e:
                return make_response(
                    jsonify({'data': {
                        'Error': str(e)
                    }}), 400
                )

            return make_response(
                jsonify({'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'token': user.encode_auth_token(user.id).decode()
                }}), 201)
        return make_response(
            jsonify({'data': {
                'Error': 'User already exists'
            }}), 409
        )

class UserAuth(Resource):
    def post(self):
        try:
            username = request.form['username']
            password = request.form['password']
            user = auth_api.login(username, password)
        except Exception:
            return make_response(
                jsonify({
                    'data': {
                        'message': 'missing username or password'
                    }}), 401)
        if user:
            return make_response(
                jsonify({'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'token': user.encode_auth_token(user.id).decode()
                }}), 200)
        else:
            return make_response(
                jsonify({
                    'data': {
                        'message': 'wrong username or password'
                    }}), 401)

def get_users(user_id):
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        return user
    else:
        users = User.query.all()
        return users


















