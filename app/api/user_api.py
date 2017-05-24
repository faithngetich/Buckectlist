import json
from flask import request, jsonify, make_response, abort
from flask_restful import Resource
from flask.views import MethodView


from app.models import db
from ..models import User
# from .auth import login


class RegisterAPI(MethodView):
    """User Registration Resource"""
    # def register(username, password):
    #     user_object = User(username=username, password=password)
    #     db.session.add(user_object)
    #     db.session.commit()
    #     return user_object
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(username=post_data.get('username')).first()
        if not user:
            try:
                user = User(
                    username=post_data.get('username'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.user_id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                    }
                results.append(responseObject)
                response = jsonify(results)
                response.status_code = 201
                return response
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

class UserAPI(Resource):
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
                'id': user.user_id,
                'username': user.username,
            }}), 200)

        else:
            return make_response(
                jsonify({'data': {
                'Error': 'User not found'
            }}), 404)

    def put(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return make_response(
                jsonify({'data': {
                'Error': 'User not found'
            }}), 404)
        # try:
        user.username = request.form['username'] or user.username,
        user.password = request.form['password'] or user.password
        db.session.add(user)
        db.session.commit()
        return make_response(
            jsonify({'data': { 'user':{
                'user_id': user.id,
                'username': user.username,
            },
            'message': 'User updated successfully'}}), 204)

        # except Exception :
        #     return make_response(
        #         jsonify({'data': {
        #             'Error': "An error has occured in your inputs"
        #         }}), 400
        #     )

    def delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
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
    def get(self):
        users = get_users(user_id=None)

        if users:
            return make_response(
                jsonify({'data': [{
                    'user_id': user.user_id,
                    'username': user.username
                } for user in users]}), 200)

        else:
            return make_response(
                jsonify({'data': {
                    'Error': 'User not found'
                }}), 404)

    # @auth.login_required
    def post(self):
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            try:
                user = User(
                    username=request.form['username'],
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
            # generate the auth token
            auth_token = user.encode_auth_token(user.user_id)
            return make_response(
                jsonify({'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'token': auth_token.decode()
                }}), 201)
        return make_response(
            jsonify({'data': {
                'Error': 'User already exists'
            }}), 409
        )

class UserAuth(Resource):
    def post(self):
        # try:
        username = request.form['username']
        password = request.form['password']
        # print (username, password)
        user = login(username, password)
        print(user)
        # except Exception:
        #     return make_response(
        #         jsonify({
        #             'data': {
        #                 'message': 'missing username or password'
        #             }}), 401)
        if user:
            return make_response(
                jsonify({'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'token': user.encode_auth_token(user.user_id).decode()
                }}), 200)
        else:
            return make_response(
                jsonify({
                    'data': {
                        'message': 'wrong username or password'
                    }}), 401)

def get_users(user_id):
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        return user
    else:
        users = User.query.all()
        return users