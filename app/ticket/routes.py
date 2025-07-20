from flask import Blueprint, flash, url_for, redirect, request, render_template
from flask_login import current_user, login_required

from app import ticket, db
from app.models import Event, Ticket

ticket_bp = Blueprint("ticket", __name__, template_folder = "templates")

@ticket_bp.route("/event/<int:event_id>/purchase",methods=['GET','POST'])
def purchase_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    # Basic Checks
    if current_user.id == event.organizer_id:
        flash("You cannot purchase a ticket for your own event!", "warning")
        return redirect(url_for('event.event_details', event_id=event.id))
    if event.status != 'upcoming':
        flash("This event is not available for purchase!", "warning")
        return redirect(url_for('event.event_details', event_id=event.id))
    if event.capacity <= 0:
        flash("This event is sold out! Sorry!!", "warning")
        return redirect(url_for('event.event_details', event_id=event.id))

    # For simplicity, we'll assume a quantity of 1 for now.
    # A form for quantity can be added later.
    quantity = 1  # Hardcoded for now

    if request.method == 'POST':
        if event.capacity < quantity:
            flash(f'Not enough tickets available for purchase. Only {event.capacity} tickets are available.', 'warning')
            return redirect(url_for('event.event_details', event_id=event.id))

        # Simulate payment (no actual payment gateway integration in this phase)

        ticket = Ticket(
            user_id=current_user.id,
            event_id=event.id,
            quantity=quantity,
        )
        event.capacity -= quantity
        db.session.add(ticket)
        db.session.commit()
        flash(f'Successfully purchased {quantity} tickets for {event.title}!', 'success')
        return redirect(url_for('ticket.my_tickets'))

    return render_template('ticket/purchase_confirm.html',titlle = 'Confirm Purchase', event=event, quantity=quantity)

@ticket_bp.route('/my_tickets')
@login_required
def my_tickets():
    user_tickets = Ticket.query.filter_by(user_id = current_user.id).order_by(Ticket.purchase_date.desc()).all()
    return render_template('ticket/my_tickets.html', title='My Tickets', tickets=user_tickets)