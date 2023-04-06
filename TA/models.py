from .main import db

class TA(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    native_english_speaker = db.Column(db.Boolean)
    course_instructor = db.Column(db.Integer)
    course = db.Column(db.Integer)
    semester = db.Column(db.Boolean)
    class_size = db.Column(db.Integer)
    performance_score = db.Column(db.Integer)


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
