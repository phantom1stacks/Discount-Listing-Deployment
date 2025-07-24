from datetime import date
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Shop(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(80), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    discounts = db.relationship("Discount", backref="shop", lazy=True)

class Discount(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    product     = db.Column(db.String(120), nullable=False)
    percent_off = db.Column(db.Integer, nullable=False)
    category    = db.Column(db.String(50), nullable=False)
    start_date  = db.Column(db.Date, nullable=False, default=date.today)
    end_date    = db.Column(db.Date, nullable=False)
    city        = db.Column(db.String(80), nullable=False)
    shop_id     = db.Column(db.Integer, db.ForeignKey("shop.id"), nullable=False)
