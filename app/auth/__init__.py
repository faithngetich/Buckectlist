from app.models import User

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user
    return False

def identity(payload):
    user_id = payload['identity']
    return User.query.filter(user_id == user_id).first()

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        return user
    return False
