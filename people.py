from flask import make_response, abort
from config import db
from models import Person, person_schema, people_schema


def read_all():
    people = Person.query.all()
    return people_schema.dump(people)

def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person not found for last name: {lname}")

def create(person):
    lname = person.get("lname")
    existing_person = (
        Person.query.filter(Person.lname == lname)
        .one_or_none()
    )

    if existing_person is None:
        schema = person_schema.load(person, session=db.session)
        db.session.add(schema)
        db.session.commit()

        return person_schema.dump(schema), 201
    else:
        abort(409, f"Person {lname} exists already")

def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is not None:
        schema = person_schema.load(person, session=db.session)
        schema.lname = existing_person.lname
        db.session.merge(schema)
        db.session.commit()

        return person_schema.dump(schema), 200
    else:
        abort(404, f"Person {lname} not found")


def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is not None:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"Person {lname} deleted", 200)
    else:
        abort(404, f"Person {lname} not found")

