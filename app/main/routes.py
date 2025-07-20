from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user

from app.models import Event

main_bp = Blueprint('main', __name__, template_folder = 'templates')

@main_bp.route('/')
@main_bp.route('/home')
def home():
    # Fetch events - order by start time, filter upcomming/active
    events = Event.query.filter(Event.end_time > datetime.utcnow()).order_by(Event.start_time.asc()).all()
    return render_template('main/home.html',title='Home', events=events)

@main_bp.route('/dashboard')
def dashboard():
    events = []
    if hasattr(current_user, 'id') and current_user.role == 'organizer':
        events = Event.query.filter_by(organizer_id=current_user.id).all()
    return render_template('main/dashboard.html',title='Dashboard',events=events)