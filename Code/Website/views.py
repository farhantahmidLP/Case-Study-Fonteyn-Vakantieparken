from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import TicketPurchase, TicketPrice, Changesz
from . import db
from datetime import datetime


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/buy-tickets', methods=['GET', 'POST'])
@login_required
def buy_tickets():
    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type')
        num_adults = int(request.form.get('num-adults', 0))
        num_children = int(request.form.get('num-children', 0))
        park_name = request.form.get('park-name')
        ticket_price = TicketPrice.query.filter_by(ticket_type=ticket_type).first()
        if ticket_price is not None:
            total_price = ticket_price.price * (num_adults + num_children)
            purchase = TicketPurchase(park=park_name, num_adults=num_adults, num_children=num_children, 
                                    total_price=total_price, user_id=current_user.id, ticket_price=ticket_price)
            db.session.add(purchase)
            db.session.commit()
            flash(f'Thank you for your purchase of {num_adults} adult(s) and {num_children} child(ren) ticket(s) for {park_name}!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid ticket type.', category='error')
    return render_template('tickets.html', user=current_user)

@views.route('/changes', methods=['GET', 'POST'])
@login_required
def changes():
    change = None  # Initialize the change variable
    if request.method == 'POST':
        data = request.form['data']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')
        is_public = 'is_public' in request.form
        change = Changesz(data=data, date=date, user_id=current_user.id, is_public=is_public)
        db.session.add(change)
        db.session.commit()
        flash('Change request added successfully', category='success')
        return redirect(url_for('views.changes'))
    changes = Changesz.query.filter_by(user_id=current_user.id).all()
    return render_template("changes.html", user=current_user, changes=changes, change=change)

@views.route('/changes/<int:id>', methods=['POST'])
@login_required
def edit_change(id):
    change = Changesz.query.get(id)
    change.data = request.form["data"]
    db.session.commit()
    return redirect(url_for('views.changes'))

@views.route('/changes/<int:id>/make_public', methods=['POST'])
@login_required
def make_public(id):
    change_id = request.form["change_id"]
    change = Changesz.query.get(change_id)
    change.is_public = True
    db.session.commit()
    flash('Change is now public!', category='success')
    return redirect(url_for('views.changes'))

@views.route('/changes/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_change(id):
    change = Changesz.query.get(id)
    db.session.delete(change)
    db.session.commit()
    return redirect(url_for('views.changes'))