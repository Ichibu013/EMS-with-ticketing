from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required


from app import db
from app.forms import EventForm
from app.models import Event

event_bp = Blueprint("event", __name__, template_folder = "templates")

# Helper Function to check role
def organizer_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['organizer', 'admin']:
            flash("You are not authorized to view this page", "danger")
            return redirect(url_for('main.home'))
        return f(*args,**kwargs)
    return decorated_function

@event_bp.route('/event/new', methods=['GET','POST'])
@organizer_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            capacity=form.capacity.data,
            ticket_price=form.ticket_price.data,
            organizer_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash("Your event has been created!", "success")
        return redirect(url_for('event.create_event'))
    return render_template('event/create_event.html', title='Create Event', form=form, legend='New Event')

@event_bp.route('/event/<int:event_id>/', methods=['GET','POST'])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event/event_deatils.html', title=event.title, event=event)

@event_bp.route('/event/<int:event_id>/update', methods=['GET','POST'])
@organizer_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id and current_user.role != 'admin':
        abort(403) #Forbiden access
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.location = form.location.data
        event.capacity = form.capacity.data
        event.ticket_price = form.ticket_price.data
        db.session.commit()
        flash("Your event has been updated!", "success")
        return redirect(url_for('event.event_details', event_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
        form.location.data = event.location
        form.capacity.data = event.capacity
        form.ticket_price.data = event.ticket_price
    return render_template('event/create_event.html', title='Update Event', form=form, legend='Update Event')

@event_bp.route('/event/<int:event_id>/delete', methods = ['POST'])
@organizer_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id and current_user.role != 'admin':
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash("Your event has been deleted!", "success")
    return redirect(url_for('main.home'))
