from . import routes_api
from app.api import user_api, bucketlist_api

# USERS
# POST
# Registers and gets users
routes_api.add_resource(user_api.UsersList, '/users')
# routes_api.add_resource(user_api.UserAuth, '/auth/register')
# routes_api.add_resource(user_api.UserAuth, '/auth/register')

routes_api.add_resource(user_api.RegisterAPI,'/auth/register')
# GET specific user
routes_api.add_resource(user_api.UserAPI, '/users/<int:user_id>')


# BUCKETLISTS
# POST & GET of bucketlist
routes_api.add_resource(bucketlist_api.AddBucketlistResource, '/bucketlists')
# POST bucketlists items
routes_api.add_resource(bucketlist_api.AddItemResource, '/bucketlists/<int:bucketlist_id>/items')
# PUT & DELETE bucketlist and item 
routes_api.add_resource(bucketlist_api.DeleteUpdateItem, '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
routes_api.add_resource(bucketlist_api.DeleteUpdateBucketList, '/bucketlists/<int:bucketlist_id>')


