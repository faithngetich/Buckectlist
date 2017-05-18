from . import routes_api
from app.api import user_api

routes_api.add_resource(user_api.UserAuth, '/users/login')
routes_api.add_resource(user_api.UsersList, '/users')
routes_api.add_resource(user_api.UserAPI, '/users/<int:user_id>')
