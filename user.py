from flask import make_response, abort
from config import db
from models import User, UserSchema
from auth_helper import verify_plymouth_auth, create_token

def read_all():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)

def read_one(user_id):
    user = User.query.filter(User.id == user_id).one_or_none()

    if user is not None:
        user_schema = UserSchema()
        return user_schema.dump(user)
    else:
        abort(404, f"User not found for Id: {user_id}")

def create(body):
    username = body.get("username")
    email = body.get("email")
    
    existing_user = (
        User.query.filter(
            (User.username == username) | (User.email == email)
        ).one_or_none()
    )

    if existing_user is None:
        schema = UserSchema()
        new_user = schema.load(body, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return schema.dump(new_user), 201
    else:
        abort(409, f"User with username {username} or email {email} exists already")

def update(user_id, user):
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        schema = UserSchema()
        update_user = schema.load(user, session=db.session)
        update_user.id = existing_user.id
        db.session.merge(update_user)
        db.session.commit()
        return schema.dump(update_user), 200
    else:
        abort(404, f"User {user_id} not found")

def delete(user_id):
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"User {user_id} deleted", 200)
    else:
        abort(404, f"User {user_id} not found")

def auth_user(body):
    username = body.get("username")
    password = body.get("password")
    
    # First verify with Plymouth authentication
    if not verify_plymouth_auth(username, password):
        abort(401, "Invalid credentials")
    
    # Then get or create local user
    user = User.query.filter(User.username == username).one_or_none()
    if user is None:
        # Create new user if they don't exist locally
        schema = UserSchema()
        new_user = schema.load({
            "username": username,
            "email": f"{username}@students.plymouth.ac.uk",
            "password": "placeholder"  # actual password is managed by Plymouth
        }, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        user = new_user
    
    # Generate JWT token
    token = create_token(user.id)
    return {"token": token}, 200