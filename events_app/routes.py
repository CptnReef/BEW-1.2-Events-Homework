"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    # TODO: Get all events and send to the template
    events =  db.session.query(Event).all()
    print(events)
    return render_template('index.html',events=events)


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    # TODO: Get the event with the given id and send to the template
    event = db.session.query(Event).get(event_id)
    return render_template('event_detail.html',event=event)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # TODO: Get the event with the given id from the database
    event = db.session.query(Event).get(event_id)

    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')

    if is_returning_guest:
        # TODO: Look up the guest by name, and add the event to their 
        # events_attending, then commit to the database
        guest = db.session.query(Guest).filter_by(name=guest_name).first()
        guest.events_attending.append(event)
        db.session.commit()
    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')
        # TODO: Create a new guest with the given name, email, and phone, and 
        # add the event to their events_attending, then commit to the database
        new_guest = Guest(
            name=guest_name,
            email=guest_email,
            phone=guest_phone
        )
        db.session.add(new_guest)
        new_guest.events_attending.append(event)
        db.session.commit()

    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        time = request.form.get('time')
        date = request.form.get('date')
        date_and_time = None
        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            print('there was an error: incorrect datetime format')

        # TODO: Create a new event with the given title, description, & 
        # datetime, then add and commit to the database
        new_event = Event(
            title=new_event_title,
            description=new_event_description,
            date_and_time=date_and_time
        )
        db.session.add(new_event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # TODO: Get the guest with the given id and send to the template
    guest = db.session.query(Guest).get(guest_id)
    return render_template('guest_detail.html', guest=guest)
