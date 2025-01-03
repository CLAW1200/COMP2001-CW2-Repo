from flask import make_response, abort
from config import db
from models import User

def auth_user(username, password):
    user = User.query.filter(User.username == username).one_or_none()
    if user is not None and user.password == password:
        return True
    else:
        return False