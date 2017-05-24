# Bucketlist resource
from flask import Flask
from flask_restful import Api, Resource, fields, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from app.models import db
from app.models.models import User, BucketList
from flask import request, jsonify

from app.api.validate import validate_register, validate_bucketlist, validate_item, validate_limit_and_offset



class AddBucketlistResource(Resource):
    # @auth.login_required
    def post(self):
        '''create new bucketlist'''
        response = {}
        json = request.json
        print(json)
        # import pdb;pdb.set_trace()
        validation = validate_bucketlist(json)
        if validation.status:
            # bucketlist = BucketList(name=json['name'],created_by=user[0].id)
            bucketlist = BucketList(name=json['name'], owner_id=current_identity.user_id)
            # current_identity.bucketlists.append(bucketlist)
            db.session.add(bucketlist)
            db.session.commit()
            status_code = 201
        else:
            status_code = 400

        response["message"] = validation.message
        response = jsonify(response)
        response.status_code = status_code
        return response

    def get(self):
        '''List all created bucketlist by name'''
        response = {}
        query = request.args.get('q') # search string
        limit = request.args.get('limit')
        # offset = request.args.get('offset')

        if limit:
            validation = validate_limit_and_offset(limit)
            if validation.status:
                # response["bucketlists"] = current_identity.get_bucketlist_as_json(limit, offset)
                bucketlists = BucketList.query.filter(BucketList.name.like(query.limit)).filter_by(owner_id=current_identity.user_id.all())
                response["meta"] = {}
                status_code = 200

                if len(response["bucketlist"]) < 1:
                    status_code = 404
                    response["message"] = "no bucketlist exists"
            else:
                status_code = 400
                response["message"] = "Invalid format of offset or limit, They should be integers"
        elif query is not None and len(name) > 0: # carry out the search
            response["bucketlists"] = []
            name = name.lower()
            query = "%" + name + "%"
            bucketlists = BucketList.query.filter(BucketList.name.like(query)).filter_by(owner_id=current_identity.user_id).all()

            if bucketlists:
                for bucketlist in bucketlists:
                    response["bucketlists"].append(bucketlist.to_json())

                status_code = 200

            else:
                status_code = 404
                response["message"] = "No bucketlist found by that name"
        else:
            status_code = 400
        
        response = jsonify(response)
        response.status_code = status_code
        return response

    def get_single(self, buckeclist_id):
        '''get a single bucketlist with specified id'''
        response = {}
        response["bucketlist"] = {}
        response["meta"] = {}
        user_id = current_identity.user_id
        bucketlist = BucketList.query.filter(bucketlist_id == BucketList.bucketlist_id, user_id == BucketList.owner_id).first()

        status_code = 200
        if buckeclist_id is not None:
            response["bucketlist"] = bucketlist.to_json()
        else:
            response["message"] = "The requested bucketlist does not exists"

        response = jsonify(response)
        response.status_code = status_code
        return response

class DeleteUpdateBucketList(Resource):
    def put(self,bucketlist_id, item_id):
        """Make changes to a bucketlist items"""
        response = {}
        json = request.json
        valiadation = validate_item(json)
        print(json)
        user_id = current_identity.user_id
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id, owner_id=user_id).first()
        q = session.query(User).filter(User.name.like('e%')).limit(5)

        bucketlist_item = None

        if bucketlist is not None:
            bucketlist_item = bucketlist.get_item(item_id)
        print(validation.message)
        if bucketlist_item is not None:
            if valiadation.status:
                bucketlist_item.from_json(json)
                db.session.commit()
                valiadation.message = "Bucketlist item {}, successfully updated".format(item_id)
                status_code = 200
            else:
                status_code = 400
        else:
            status_code = 200
            validation.message = "The requested bucketlist or bucketlist item does not exist."

        response["message"] = valiadation.message
        response.status_code = status_code
        return response

    def delete(self, bucketlist_id, item_id):
        """Delete a bucketlist item from a bucketlist"""
        response = {}
        user_id = current_identity.user_id
        bucketlist = Bucketlist.query.filter_by(bucketlist_id, owner_id=user_id)

        bucketlist_item = None

        if bucketlist_item is not None:
            bucketlist_item = bucketlist.get_item(item_id)
            
        if bucketlist_item is not None:
            db.session.delete(bucketlist_item)
            status_code = 200
            response["message"] = "The bucketlist item with id {} has been deleted.".format(item_id)
            db.session.commit()
        else:
            status_code = 200
            response["message"] = "The bucketlist or bucketlist item does not exist."

        response = jsonify(response)
        response.status_code = status_code
        return response

class AddItemResource(Resource):
    
    def add_bucketlist_item(bucketlist_id):
        '''Create a bucketlist item and add it to bucketlist with given id'''
        response = {}
        json = request.json
        validation = validate_item(json)

        user_id = current_identity.user_id
        bucketlist = BucketList.query.filter(
            bucketlist_id == BucketList.bucketlist_id,
            user_id == BucketList.owner_id
        ).first()

        if bucketlist is not None:
            if validation.status:
                item = ListItem(item_name=json['name'])
                bucketlist.items.append(item)
                db.session.add(item)
                db.session.commit()
                status_code = 201
            else:
                status_code = 400
        else:
            status_code = 200
            validation.message = "The requested bucketlist does not exist."

        response["message"] = validation.message
        response = jsonify(response)
        response.status_code = status_code
        return response

class DeleteUpdateItem(Resource):
    def update_bucketlist_item(bucketlist_id, item_id):
        '''Make changes to a bucketlist item'''
        response = {}
        json = request.json
        validation = validate_item(json)
        print(json)
        user_id = current_identity.user_id
        bucketlist = BucketList.query.filter_by(bucketlist_id=bucketlist_id,owner_id=user_id).first()

        bucketlist_item = None

        if bucketlist is not None:
            bucketlist_item = bucketlist.get_item(item_id)
        print(validation.message)
        if bucketlist_item is not None:
            if validation.statsus:
                bucketlist_item.from_json(json)
                db.session.commit()
                validation.message = "Bucketlist item %d successfully updated!" % (
                    item_id)
                status_code = 200
            else:
                status_code = 400
        else:
            status_code = 200
            validation.message = "The requested bucketlist or bucketlist item does not exist."

        response["message"] = validation.message
        response = jsonify(response)
        response.status_code = status_code
        return response

    def delete_item_from_bucketlist(bucketlist_id, item_id):
        '''Delete bucketlist item from a bucketlist'''
        response = {}
        user_id = current_identity.user_id
        bucketlist = BucketList.query.filter_by(
            bucketlist_id=bucketlist_id,
            owner_id=user_id
        ).first()

        bucketlist_item = None

        if bucketlist is not None:
            bucketlist_item = bucketlist.get_item(item_id)

        if bucketlist_item is not None:
            db.session.delete(bucketlist_item)
            status_code = 200
            response["message"] = "The bucketlist item with id %d has been deleted" % (
                item_id)
            db.session.commit()
        else:
            status_code = 200
            response["message"] = "The bucketlist or bucketlist item does not exist."

        response = jsonify(response)
        response.status_code = status_code
        return response

# class Bucketlist(Resource):
#     def get(self):
#         """Get all the bucketlist of the user in hierachy"""
#         q = db.session.query
#         result = {}
#         users = q(Users).all()
#         for person in users:
#             result[person.name] = _get_bucketlist_tree(q, person)
#         return result

#     def post(self):
#         # parse the arguments
#         parser = reqparse.RequestParser()
#         parser.add_argument('user', type=str, required=True)
#         parser.add_argument(, type=str, required=True)
#         parser.add_argument('password', type=str, required=True)
#         parser.add_argument('bucketlist', type=str, required=False)
#         # Get a SQL Alchemy query object
#         q = db.session.querry
#         # Create a new bucketlist
#         user = q(Bucketlist).filter_by(name=args.name).one()
#         # find by name
#         bucketlist = q.Bucketlist(user=user,name=args.name)
#         db.session.add(bucketlist)
#         db.session.commit()

#     def put(self):
#         """ Update end time"""
#         parser = RequestParser()
#         parser.add_argument('user_name', type=str, required=True)
#         args = parser.parse_args()
#         # Get a SQL Alchemy query object
#         q = db.session.querry
#         bucketlist = q(Bucketlist).filter_by(name=args.name).one()
#         bucketlist.end = datetime.now()
#         db.session.commit()
    
        
