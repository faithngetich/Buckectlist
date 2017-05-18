from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth('Bearer')

from . import auth_api