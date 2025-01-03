from flask import make_response, abort
from config import db
from models import Trail, TrailSchema

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

def create(trail):
    name = trail.get("name")
    existing_trail = (
        Trail.query.filter(Trail.name == name)
        .one_or_none()
    )

    if existing_trail is None:
        schema = TrailSchema().load(trail, session=db.session)
        db.session.add(schema)
        db.session.commit()

        return TrailSchema().dump(schema), 201
    else:
        abort(409, f"Trail {name} exists already")

def update(trail_id, trail):
    existing_trail = Trail.query.filter(Trail.id == trail_id).one_or_none()

    if existing_trail is not None:
        schema = TrailSchema().load(trail, session=db.session)
        schema.id = existing_trail.id
        db.session.merge(schema)
        db.session.commit()

        return TrailSchema().dump(schema), 200
    else:
        abort(404, f"Trail {trail_id} not found")


def delete(trail_id):
    existing_trail = Trail.query.filter(Trail.id == trail_id).one_or_none()

    if existing_trail is not None:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"Trail {trail_id} deleted", 200)
    else:
        abort(404, f"Trail {trail_id} not found")

