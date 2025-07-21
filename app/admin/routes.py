from functools import wraps

from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app import db
from app.models import User, Event

admin_bp = Blueprint("admin", __name__, template_folder = "templates")

# Role Check helper function
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args,**kwargs):
        if current_user.role != 'admin':
            flash("You are not authorized to view this page", "danger")
            return redirect(url_for('main.home'))
        return f(*args,**kwargs)
    return decorated_function

@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.all()
    events = Event.query.all()
    return render_template('admin/dashboard.html', title='Admin Dashboard', users=users, events=events)

@admin_bp.route('/admin/users/<int:user_id>/delete', methods = ['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete yourself!", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    event = Event.query.filter_by(organizer_id = user.id).first()
    if event:
        flash("You cannot delete a user who has created an event!", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been successfully deleted', "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/events/<int:event_id>/delete', methods = ['POST'])
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash(f'Event {event.title} has been successfully deleted', "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/users/<int:user_id>/set_role', methods = ['POST'])
@admin_required
def set_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('new_role')
    if new_role not in ['organizer', 'admin', 'attendee']:
        flash("Invalid role", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    if user.id == current_user.id and new_role != 'admin':
        flash("You cannot demote your own role!", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    user.role = new_role
    db.session.commit()
    flash(f'Role for {user.username} has been successfully updated', "success")
    return redirect(url_for('admin.admin_dashboard'))