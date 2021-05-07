"""Create database models to represent tables."""
import enum
from events_app import db
from sqlalchemy.orm import backref

# TODO: Create a model called `Guest` with the following fields:
# - id: primary key
# - name: String column
# - email: String column
# - phone: String column
# - events_attending: relationship to "Event" table with a secondary table

class Guest(db.Model):
    #SQL Error??
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    events_attending = db.relationship('Event', back_populates="guests", secondary='guest_event_table')

# TODO: Create a model called `Event` with the following fields:
# - id: primary key
# - title: String column
# - description: String column
# - date_and_time: DateTime column
# - guests: relationship to "Guest" table with a secondary table

# STRETCH CHALLENGE: Add a field `event_type` as an Enum column that denotes the
# type of event (Party, Study, Networking, etc)
class EVENT_TYPE(enum.Enum):
    Party = "Party"
    Study = "Study"
    Networking = "Networking"   
    etc = "etc"

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(80))
    date_and_time = db.DateTime(db.DateTime())
    event_type = db.Column(db.Enum(EVENT_TYPE))
    guests = db.relationship('Guest', back_populates="events_attending", secondary='guest_event_table')

# TODO: Create a table `guest_event_table` with the following columns:
# - event_id: Integer column (foreign key)
# - guest_id: Integer column (foreign key)

class Guest_Event_Table(db.Model):
    __tablename__ = 'guest_event_table'

    event_id = db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)
    guest_id = db.Column('guest_id', db.Integer, db.ForeignKey('guests.id'), primary_key=True)
