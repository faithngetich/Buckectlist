import re
from app.models.models import BucketList, Item


class Validation:
    '''Class for returning validation results'''
    def __init__(self):
        self.status = None
        self.message = ""


def validate_register(json):
    keys = ['username','password']
    validation = Validation()
    for field in keys:
        if field not in json.keys():
            validation.status = False
            validation.message = "Missing fields in request data. Include: " +\
                ", ".join(keys)
            return validation

    if len(json['password']) < 8:
        validation.status = False
        validation.message = "The password should be more than 8 characters."
        return validation
    # ^ marks the start of the string
    # $ end of the line
    match = re.match('^[0-9]{2}-[0-9]{3}$',json["username"])
    if match is None:
        validation.status = False
        validation.message = "username is invalid"
        return validation

    validation.status = True
    validation.status = "User successfully registered."
    return validation


def validate_bucketlist(json):
    validation = Validation()
    try:
        if not len(json['name']):
            validation.status = False
            validation.message = "The bucketlist name is too short."
            return validation
        else:
            bucketlist = BucketList.query.filter_by(name=json['name']).first()
            if bucketlist:
                validation.status = False
                validation.message = "Bucketlist already exists"
                return validation
            else:              
                validation.status = True
                validation.message = "Bucketlist successfully created!"
                return validation
                # validation.status = True
                # validation.message = "Bucketlist successfully created!"
            
    except KeyError:
        validation.status = False
        validation.message = "You did not include a bucketlist name."
        return validation
    # else:
    #     validation.status = False
    #     validation.message = "Bucketlist already exists"
    #     return validation

def validate_item(json):
    validation = Validation()
    try:
        if not len(json['item_name']):
            validation.status = False
            validation.message = "The item name is too short."
            return validation
        else:
            item = Item.query.filter_by(item_name=json['item_name']).first()
            if item:
                validation.status = False
                validation.message = "Item already exists"
                return validation
            else:              
                validation.status = True
                validation.message = "Item successfully created!"
                return validation
    except KeyError:
        validation.status = False
        validation.message = "You did not include an Item name."
        return validation
            
    #     if json.item_name:
    #         validation.status = False
    #         validation.message = "Invalid data."
    #         return validation
    #     if 'name' in json and not len(json['name']) > 0:
    #         validation.status = False
    #         validation.message = "The item name is too short."
    #     elif 'done' in json and not json['done'] in ['true', 'false']:
    #         validation.status = False
    #         validation.message = "The item completion status should be either 'true' or 'false'."
    #     else:
    #         validation.status = True
    #         validation.message = "Item successfully created!"
    #     return validation
    # except KeyError:
    #     validation.status = False
    #     validation.message = "You did not include the item name."
    #     return validation


def validate_limit_and_offset(limit='20', offset=100):
    validation = Validation()
    try:
        limit = int(limit)
        offset = int(offset)
    except ValueError:
        validation.status = False
    if limit > offset:
        validation.status = False
    elif limit < 1:
        validation.status = False
    validation.status = True
    return validation