from . import db
from datetime import date, datetime

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100))