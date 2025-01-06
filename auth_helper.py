import requests
from functools import wraps
from flask import request, abort
import jwt
from config import app

SECRET_KEY = "a-super-secret-key"
AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def get_auth_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'Bearer ' not in auth_header:
        abort(401, "Missing or invalid authorization token")
    return auth_header.split(' ')[1]

def verify_plymouth_auth(username, password):
    try:
        response = requests.post(AUTH_URL, json={
            "username": username,
            "password": password
        })
        return response.status_code == 200
    except:
        return False

def create_token(user_id):
    return jwt.encode(
        {'user_id': user_id},
        SECRET_KEY,
        algorithm='HS256'
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_auth_token()
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user_id = payload['user_id']
            return f(*args, **kwargs)
        except jwt.InvalidTokenError:
            abort(401, "Invalid token")
    return decorated 