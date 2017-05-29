from . import routes_api
from app.api import user_api, bucketlist_api

# USERS
# POST
# routes_api.add_resource(user_api.UserAuth, '/auth/login')
routes_api.add_resource(user_api.UserAPI,'/auth/register')

# BUCKETLISTS
# POST & GET of bucketlist
routes_api.add_resource(bucketlist_api.AddBucketlistResource, '/bucketlists')
routes_api.add_resource(bucketlist_api.GetSingleBucketlistById, '/bucketlists/<int:id>')

# POST bucketlists items
routes_api.add_resource(bucketlist_api.AddItemResource, '/bucketlists/<int:bucketlist_id>/items')
# PUT & DELETE bucketlist and item 
routes_api.add_resource(bucketlist_api.DeleteUpdateItem, '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
routes_api.add_resource(bucketlist_api.DeleteUpdateBucketList, '/bucketlists/<int:bucketlist_id>')


