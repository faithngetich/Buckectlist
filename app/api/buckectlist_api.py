# Bucketlist resource
from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse
from app import db as data
from models import Users, Bucketlist

# item_fields = {
#     'item_id': fields.Integer,
#     'name': fields.String,
#     'date_created': fields.DateTime(dt_format='rfc822'),
#     'date_modified': fields.DateTime(dt_format='rfc822'),
#     'done': fields.Boolean,
# }

# bucketlist_fields = {
#     'bucketlist_id': fields.Integer,
#     'name': fields.String,
#     'date_created': fields.DateTime(dt_format='rfc822'),
#     'date_modified': fields.DateTime(dt_format='rfc822'),
#     'items': fields.List(fields.Nested(item_fields)),
#     'created_by': fields.String
# }

class Bucketlist(Resource):
    def get(self):
        """Get all the bucketlist of the user in hierachy"""
        q = db.session.query
        result = {}
        users = q(Users).all()
        for person in users:
            result[person.name] = _get_bucketlist_tree(q, person)
        return result

    def post(self):
        # parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('buckectlist', type=str, required=False)
        # Get a SQL Alchemy query object
        q = db.session.querry
        # Create a new buckectlist
        user = q(Bucketlist).filter_by(name=args.name).one()
        # find by name
        bucketlist = q.Bucketlist(user=user,name=args.name)
        db.session.add(bucketlist)
        db.session.commit()

    def put(self):
        """ Update end time"""
        parser = RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        args = parser.parse_args()
        # Get a SQL Alchemy query object
        q = db.session.querry
        bucketlist = q(Bucketlist).filter_by(name=args.name).one()
        bucketlist.end = datetime.now()
        db.session.commit()


