from flask import make_response, abort
from config import db
from models import Location, LocationSchema

def read_all():
    locations = Location.query.all()
    location_schema = LocationSchema(many=True)
    return location_schema.dump(locations)

def read_one(location_id):
    location = Location.query.filter(Location.id == location_id).one_or_none()

    if location is not None:
        location_schema = LocationSchema()
        return location_schema.dump(location)
    else:
        abort(404, f"Location not found for Id: {location_id}")

def create(body):
    schema = LocationSchema()
    new_location = schema.load(body, session=db.session)
    db.session.add(new_location)
    db.session.commit()
    return schema.dump(new_location), 201

def update(location_id, body):
    existing_location = Location.query.filter(Location.id == location_id).one_or_none()

    if existing_location is not None:
        schema = LocationSchema()
        update_location = schema.load(body, session=db.session)
        update_location.id = existing_location.id
        db.session.merge(update_location)
        db.session.commit()
        return schema.dump(update_location), 200
    else:
        abort(404, f"Location {location_id} not found")

def delete(location_id):
    existing_location = Location.query.filter(Location.id == location_id).one_or_none()

    if existing_location is not None:
        db.session.delete(existing_location)
        db.session.commit()
        return make_response(f"Location {location_id} deleted", 200)
    else:
        abort(404, f"Location {location_id} not found")