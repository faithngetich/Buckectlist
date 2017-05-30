from flask import Blueprint
from flask_restful import Api

routes = Blueprint('routes', __name__)
routes_api = Api(routes)

from . import user_bucket_routes