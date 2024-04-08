from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, TicketPurchase
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('E-mail does not exist!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('E-mail already in use!', category='error')
        elif len(email) < 4:
            flash('E-mail must be greater than 3 characters!', category='error')
        elif len(first_name) < 2:
            flash('Your first name must be greater than 1 character!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(password1) < 7:
            flash('Password is too short, must be atleast 7 characters!', category='error')
        else:
            user = User(email=email, first_name=first_name, admin=0)
            user.password = generate_password_hash(password1)
            db.session.add(user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/admin')
@login_required
def admin():
    if current_user.admin == 1:
        users = User.query.all()
        return render_template("admin.html", users=users, user=current_user)
    else:
        flash('You\'re not an administrator!', category='error')
        return redirect(url_for('views.home'))

@auth.route('/edit_admin', methods=['GET', 'POST'])
@login_required
def edit_admin():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.phone_number = request.form.get('phone_number')
        user.age = request.form.get('age')
        user.nationality = request.form.get('nationality')
        user.bio = request.form.get('bio')
        db.session.commit()
        flash('Admin information successfully updated!', category='success')
        return redirect(url_for('auth.admin'))
    else:
        return render_template('admin.html')

@auth.route('/changepass', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']

        if new_password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('views.home'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully')
        return redirect(url_for('views.home'))

    return render_template("changepass.html", user=current_user)

@auth.route('/refund/<int:ticket_id>', methods=['POST'])
@login_required
def refund_ticket(ticket_id):
    ticket = TicketPurchase.query.filter_by(id=ticket_id).first()
    if ticket:
        ticket.is_refunded = True
        db.session.commit()
        flash('Ticket refunded successfully!', category='success')
    else:
        flash('Ticket not found!', category='error')
    return redirect(url_for('auth.profile'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)