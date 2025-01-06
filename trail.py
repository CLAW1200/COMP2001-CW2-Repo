from flask import make_response, abort, request
from config import db
from models import Trail, TrailSchema
from auth_helper import requires_auth

def read_all():
    trails = Trail.query.all()
    trail_schema = TrailSchema(many=True)
    return trail_schema.dump(trails)

def read_one(trail_id):
    trail = Trail.query.filter(Trail.id == trail_id).one_or_none()

    if trail is not None:
        trail_schema = TrailSchema()
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail not found for Id: {trail_id}")

@requires_auth
def create(body):
    name = body.get("name")
    existing_trail = (
        Trail.query.filter(Trail.name == name)
        .one_or_none()
    )

    if existing_trail is None:
        schema = TrailSchema()
        new_trail = schema.load(body, session=db.session)
        new_trail.owner_id = request.current_user_id  # Set owner to current user
        db.session.add(new_trail)
        db.session.commit()
        return schema.dump(new_trail), 201
    else:
        abort(409, f"Trail {name} exists already")

@requires_auth
def update(trail_id, trail):
    existing_trail = Trail.query.filter(Trail.id == trail_id).one_or_none()

    if existing_trail is None:
        abort(404, f"Trail {trail_id} not found")
    
    # Check ownership
    if existing_trail.owner_id != request.current_user_id:
        abort(403, "Not authorized to modify this trail")

    schema = TrailSchema()
    update_trail = schema.load(trail, session=db.session)
    update_trail.id = existing_trail.id
    update_trail.owner_id = request.current_user_id
    db.session.merge(update_trail)
    db.session.commit()
    return schema.dump(update_trail), 200

@requires_auth
def delete(trail_id):
    existing_trail = Trail.query.filter(Trail.id == trail_id).one_or_none()

    if existing_trail is None:
        abort(404, f"Trail {trail_id} not found")
    
    # Check ownership
    if existing_trail.owner_id != request.current_user_id:
        abort(403, "Not authorized to delete this trail")

    db.session.delete(existing_trail)
    db.session.commit()
    return make_response(f"Trail {trail_id} deleted", 200)

