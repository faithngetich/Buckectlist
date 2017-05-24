import jwt
from flask import Flask
from flask_jwt import JWT

from .config import config_by_name
from .auth import identity, authenticate, login
from app.models import db

jwt = JWT()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)


    from app.routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint, url_prefix='/api')

    jwt.authentication_callback = authenticate
    jwt.identity_callback = identity
    jwt.init_app(app)
    return app