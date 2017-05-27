# Bucketlist resource
from flask import Flask
from app.models import db
from flask_restful import Api, Resource, fields, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from app.models.models import User, BucketList, Item
from flask import request, jsonify, make_response
from app.api.validate import validate_register, validate_bucketlist, validate_item, validate_limit_and_offset


class AddBucketlistResource(Resource):
    decorators =[jwt_required()]
    def post(self):
        '''create new bucketlist'''
        response = {}
        json = request.json
        print(json)
        validation = validate_bucketlist(json)

        if validation.status:
            bucketlist = BucketList(name=json['name'], created_by=current_identity.id)
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
        query = request.args.get('q', None) # search string
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', None)

        if not (offset or limit):
            bucketlists = BucketList.query.filter_by(created_by=current_identity.id).all()
            print(bucketlists)
            blists = []
            for blist in bucketlists:
                blist_object = {
                    "id": blist.bucketlist_id,
                    "name": blist.name,
                    "date_created": blist.date_created,
                    "date_modified": blist.date_modified
                }
                blists.append(blist_object);
            response = jsonify({
                "bucketlists": blists
            })
            return make_response(response, 200)

        if offset and limit:
            validation = validate_limit_and_offset(limit, offset)
            if validation.status:
                bucketlists = paginate(offset, limit)
                response = {}
                status_code = 200
                response["bucketlist"] = bucketlists
                response['status'] = status_code

                if len(response["bucketlist"]) < 1:
                    status_code = 404
                    response["message"] = "no bucketlist exists"
                    response['status'] = status_code
                    
                blists = []
                for blist in bucketlists:
                    blist_object = {
                        "id": blist.bucketlist_id,
                        "name": blist.name,
                        "date_created": blist.date_created,
                        "date_modified": blist.date_modified
                    }
                    blists.append(blist_object);
                response = jsonify({
                    "bucketlists": blists
                })
                return make_response(response, 200)

            else:
                status_code = 400
                response["message"] = "Invalid format of offset or limit, They should be integers"

        elif query is not None and len(name) > 0: # carry out the search
            response["bucketlists"] = []
            name = name.lower()
            query = "%" + name + "%"
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

class GetSingleBucketlistById(Resource):
    decorators =[jwt_required()]
    def get(self, id):
        '''get a single bucketlist with specified id'''
        user_id = current_identity.id
        bucketlist = BucketList.query.filter_by(created_by=current_identity.id).filter_by(bucketlist_id=id).first()
        if bucketlist:
            print(bucketlist.items)
            items_list = []
            for item in bucketlist.items:
                one_item = {
                    "item_id": item.item_id,
                    "done": item.done,
                    "item_name": item.item_name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified
                }
                items_list.append(one_item)
            blist_object = {
                "id": bucketlist.bucketlist_id,
                "name": bucketlist.name,
                "items": items_list,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified
            }
            response = jsonify({
                "bucketlists": blist_object
            })
            return make_response(response, 200)
        response = jsonify({
            "message" : "Bucketlist not found"
        })
        return make_response(response, 404)

class DeleteUpdateBucketList(Resource):
    decorators =[jwt_required()]
    def put(self, bucketlist_id):
        """Make changes to a bucketlist items"""
        user_id = current_identity.id
        bucketlist = BucketList.query.filter_by(created_by=current_identity.id).filter_by(bucketlist_id=bucketlist_id).first()
        if bucketlist:
            bucketlist.name = request.json['name']
            db.session.add(bucketlist)
            db.session.commit()
            blist_object = {
                "id": bucketlist.bucketlist_id,
                "name": bucketlist.name,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified
            }
            response = jsonify({
                "bucketlists": blist_object
            })
            return make_response(response, 200)
        response = jsonify({
            "message" : "Bucketlist not found"
        })
        return make_response(response, 404)        
    
    def delete(self, bucketlist_id):
        """Delete a bucketlist item from a bucketlist"""
        user_id = current_identity.id
        bucketlist = BucketList.query.filter_by(created_by=current_identity.id).filter_by(bucketlist_id=bucketlist_id).first()
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()

            response = jsonify({
                "bucketlist": "Bucketlist deleted successfully"
            })
            return make_response(response, 200)

        response = jsonify({
            "message" : "Bucketlist not found"
        })
        return make_response(response, 404)        
class AddItemResource(Resource):
    decorators =[jwt_required()]
    def post(self, bucketlist_id):
        '''Create a bucketlist item and add it to bucketlist with given id'''
        response = {}
        json = request.json
        print(json)
        validation = validate_item(json)
        if validation.status:
            bucketlist_item = Item(item_name=json['item_name'], bucketlist_id=bucketlist_id)
            db.session.add(bucketlist_item)
            db.session.commit()
            status_code = 201
        else:
            status_code = 400

        response["message"] = validation.message
        response = jsonify(response)
        response.status_code = status_code
        return response

class DeleteUpdateItem(Resource):
    decorators =[jwt_required()]
    def put(self, bucketlist_id, item_id):
        """Make changes to a bucketlist items"""
        user_id = current_identity.id
        bucketlist=BucketList.query.filter_by(created_by=current_identity.id).filter_by(bucketlist_id=bucketlist_id).first()
        item = Item.query.filter_by(bucketlist_id=bucketlist.bucketlist_id).first()
        print(item, bucketlist)
        if item:
            item.item_name = request.json['item_name']
            db.session.add(item)
            db.session.commit()
            item_object = {
                "item_id": item.item_id,
                "done": item.done,
                "item_name": item.item_name,
                "date_created": item.date_created,
                "date_modified": item.date_modified
            }
            response = jsonify({
                "item": item_object
            })
            return make_response(response, 200)

        response = jsonify({
            "message" : "Item not found"
        })
        return make_response(response, 404) 
    def delete_item_from_bucketlist(self, bucketlist_id, item_id):
        '''Delete bucketlist item from a bucketlist'''
        user_id = current_identity.id
        item = BucketList.query.filter_by(created_by=current_identity.id).filter_by(bucketlist_id=bucketlist_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()

            response = jsonify({
                "item": "Item deleted successfully"
            })
            return make_response(response, 200)

        response = jsonify({
            "message" : "Item not found"
        })
        return make_response(response, 404)        
    
def paginate(offset, limit):
    query = BucketList.query.filter_by(created_by=current_identity.id)
    if offset: 
        query = query.offset(offset)
    if limit:
            query = query.limit(limit)

    return query.all()