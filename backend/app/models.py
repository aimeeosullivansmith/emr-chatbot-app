from . import db
from datetime import date, datetime, timezone
import enum


# ENUM DEFINITIONS

class Status(enum.Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


# DATABASE TABLES

class patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100))
    primary_gp = db.Column(db.Integer, db.ForeignKey('gp_doctor.gmc_id'), nullable=False)
    primary_surgery = db.Column(db.Integer, db.ForeignKey('gp_surgery.id'), nullable=False)

class doctor(db.model):
    id = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100))
    speciality = db.Column(db.String(50), nullable=False)

class gp_doctor(db.model):
    id = db.Column(db.Integer, primary_key=True)
    gmc_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id'), nullable=False)

class hospital_doctor(db.model):
    id = db.Column(db.Integer, primary_key=True)
    gmc_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_department.id'), nullable=False)

class gp_surgery(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    num_employees = db.Column(db.Integer, nullable=False)

class hospital(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    num_employees = db.Column(db.Integer, nullable=False)

class hospital_department(db.model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    num_employees = db.Column(db.Integer, nullable=False)

class department(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class appointment(db.model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id')) # Two potential locations for appointment
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id')) # One is nullable
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    # Treatment Plan ID
    status = db.Column(db.Enum(Status), nullable=False, default=Status.SCHEDULED)

class procedure(db.model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    description = db.Column(db.Text)

class appointment_procedure(db.model):
    id = db.Column(db.Integer, priamry_key=True)
    # Procedure ID
    # Appointment ID
    status = db.Column(db.Enum(Status), nullable=False, default=Status.SCHEDULED)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    # Location ID
    

