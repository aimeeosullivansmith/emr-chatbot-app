from . import db
from datetime import date, datetime, timezone
import enum


# ENUM DEFINITIONS

class Status(enum.Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class TimeStatus(enum.Enum):
    ONGOING = "On-Going"
    FINISHED = "Finished"

class Result(enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

class LetterType(enum.Enum):
    REFERRAL = "Referral"
    DISCHARGE = "Discharge"
    RESULT = "Result"
    APPOINTMENT = "Appointment"
    MEDICATION = "Medication"
    ADMIN = "Administrative"
    OTHER = "Other"

class MedicationForm(enum.Enum):
    TABLET = "Tablet"
    CAPSULE = "Capsule"
    INJECTION = "Injection"
    SYRUP = "Syrup"
    CREAM = "Cream"
    INHALER = "Inhaler"
    PATCH = "Transdermal Patch"
    DROPS = "Drops"

class MedicationLength(enum.Enum):
    ACUTE = "Acute"
    REPEAT = "Repeat"

class Severity(enum.Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"    


# DATABASE TABLES

class patient(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100))
    primary_gp = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    primary_surgery = db.Column(db.Integer, db.ForeignKey('gp_surgery.id'), nullable=False)

class doctor(db.Model):
    id = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100))
    speciality = db.Column(db.String(50), nullable=False)

class gp_doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmc_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id'), nullable=False)

class hospital_doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmc_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_department.id'), nullable=False)

class gp_surgery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    num_employees = db.Column(db.Integer, nullable=False)

class hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    num_employees = db.Column(db.Integer, nullable=False)

class hospital_department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    num_employees = db.Column(db.Integer, nullable=False)

class department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id')) # two potential locations for appointment
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id')) # one is nullable
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    treatment_plan_id = db.Column(db.Integer, db.ForeignKey('treatment_plan.id'))
    status = db.Column(db.Enum(Status), nullable=False, default=Status.SCHEDULED)

class procedure(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    description = db.Column(db.Text)

class appointment_procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    procedure_id = db.Column(db.String(20), db.ForeignKey('procedure.id'), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.SCHEDULED)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id')) # two potential locations for appointment procedure
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id')) # one is nullable
    
class result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appt_procedure_id = db.Column(db.Integer, db.ForeignKey('appointment_procedure.id'), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(Result), nullable=False, default=Result.PENDING)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    tested_name = db.Column(db.String(100))
    tested_value = db.Column(db.Real)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)

class letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    recipient_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    letter_type = db.Column(db.Enum(LetterType), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    status = db.Column(db.Enum(Result), nullable=False, default=Result.PENDING)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)

class treatment_plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

class referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    referring_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    referred_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id')) # two potential locations for referral
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id')) # one is nullable
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(Result), nullable=False, default=Result.PENDING)
    referred_department = db.Column(db.Integer, db.ForeignKey('hospital_department.id')) # nullable in case referral is to gp surgery
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)

class medication(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chemical_name = db.Column(db.String(100), nullable=False)
    brand_name = db.Column(db.String(100), nullable=False)
    form = db.Column(db.Enum(MedicationForm), nullable=False)
    strength = db.Column(db.Integer, nullable=False) # might need to change for multiple values
    purpose = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

class patient_medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)
    prescribing_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    reason = db.Column(db.Text, nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    medication_id = db.Column(db.String(20), db.ForeignKey('medication.id'), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    time_period = db.Column(db.Enum(MedicationLength), nullable=False)
    status = db.Column(db.Enum(TimeStatus), nullable=False)

class vaccination(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    side_effects = db.Column(db.Text, nullable=False)

class patient_vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)
    vaccination_id = db.Column(db.String(20), db.ForeignKey('vaccination.id'), nullable=False)
    dose_number = db.Column(db.Integer, nullable=False)
    administering_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id')) # two potential locations for referral
    surgery_id = db.Column(db.Integer, db.ForeignKey('gp_surgery.id')) # one is nullable
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    lot_number = db.Column(db.String(20), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))

class allergy(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    allergen = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=False)

class patient_allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)
    allergy_id = db.Column(db.String(20), db.ForeignKey('allergy.id'), nullable=False)
    severity = db.Column(db.Enum(Severity), nullable=False)
    reaction = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    diagnosing_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    status =  db.Column(db.Enum(TimeStatus), nullable=False)

class condition(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    infectious = db.Column(db.Boolean, nullable=False)
    notes = db.Column(db.Text)

class patient_condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)
    condition_id = db.Column(db.String(20), db.ForeignKey('condition.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    status = db.Column(db.Enum(TimeStatus), nullable=False)
    severity = db.Column(db.Enum(Severity), nullable=False)
    notes = db.Column(db.Text)
    diagnosing_doctor_id = db.Column(db.String(7), db.ForeignKey('doctor.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))