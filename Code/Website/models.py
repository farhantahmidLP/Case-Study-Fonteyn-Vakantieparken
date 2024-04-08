from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func

import os, hashlib

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    nationality = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(120))
    salt = db.Column(db.String(120))
    pepper = db.Column(db.String(255))
    admin = db.Column(db.Integer, nullable=False)
    tickets = db.relationship("TicketPurchase", backref="purchased_by", lazy=True)

    def __init__(self, email, first_name, password=None, admin=0, salt=None, pepper=None):
        self.email = email
        self.first_name = first_name
        self.admin = admin
        self.salt = salt or os.urandom(32).hex()
        self.pepper = pepper or os.urandom(32).hex()
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def hash_password(self, password):
        salted_password = hashlib.sha256(self.salt.encode() + password.encode() + self.pepper.encode()).hexdigest()
        return salted_password

class TicketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

class TicketPurchase(db.Model):
    __tablename__ = "ticket_purchase"
    id = db.Column(db.Integer, primary_key=True)
    park = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    num_adults = db.Column(db.Integer, nullable=False, default=0)
    num_children = db.Column(db.Integer, nullable=False, default=0)
    total_price = db.Column(db.Float, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ticket_price_id = db.Column(db.Integer, db.ForeignKey("ticket_price.id"), nullable=False)
    user = db.relationship("User", backref="ticket_purchases")
    ticket_price = db.relationship("TicketPrice", backref="ticket_purchases")
    is_refunded = db.Column(db.Boolean, nullable=False, default=False)

class Changesz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=False)