from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from .main import app, db
from .models import User, TA
from . import auth

@app.route("/viewAll", methods=['GET'])
@auth.token_auth()
def viewAll():
    allTA = db.session.query(TA.id, TA.native_english_speaker, TA.course_instructor, TA.course, TA.semester, TA.class_size, TA.performance_score).all()
    data_list = [[item for item in tpl] for tpl in allTA]
    return jsonify(data_list)


@app.route("/viewAllId", methods=['GET'])
@auth.token_auth()
def viewAllId():
    allTAId = TA.query.filter().all()
    data_list = [item.id for item in allTAId]
    return jsonify(data_list)


@app.route("/viewWithId/<int:ta_id>", methods=['GET'])
@auth.token_auth()
def view_with_id(ta_id):
    thisTA = db.session.query(TA.id, TA.native_english_speaker, TA.course_instructor, TA.course, TA.semester, TA.class_size, TA.performance_score).filter(TA.id == ta_id).first()
    data_list = [tpl for tpl in thisTA]
    return jsonify(data_list)

@app.route("/add", methods=["POST"])
@auth.token_auth()
def add():
    from .main import str_to_bool
    ta_id = request.form.get("id")
    native_english_speaker = bool(str_to_bool(request.form.get("native_english_speaker")))
    course_instructor = request.form.get("course_instructor")
    course = request.form.get("course")
    semester = bool(str_to_bool(request.form.get("semester")))
    class_size = request.form.get("class_size")
    performance_score = request.form.get("performance_score")
    try:
        new_ta = TA(id=ta_id, native_english_speaker=native_english_speaker, course_instructor=course_instructor, course=course, semester=semester, class_size=class_size, performance_score=performance_score)
        db.session.add(new_ta)
        db.session.commit()
        return {"Success": "TA added Successfully"}
    except IntegrityError:
        db.session.rollback()
        return {"Failed": "Id already exist"}

@app.route("/update/<int:ta_id>", methods=['put', 'POST'])
@auth.token_auth()
def update(ta_id):
    native_english_speaker = bool(request.form.get("native_english_speaker"))
    course_instructor = request.form.get("course_instructor")
    course = request.form.get("course")
    semester = bool(request.form.get("semester"))
    class_size = request.form.get("class_size")
    performance_score = request.form.get("performance_score")

    existingTA = TA.query.filter(TA.id == ta_id).first()

    existingTA.native_english_speaker = native_english_speaker
    existingTA.course_instructor = course_instructor
    existingTA.course = course
    existingTA.semester = semester
    existingTA.class_size = class_size
    existingTA.performance_score = performance_score

    db.session.commit()
    return {"Success": "TA Updated Successfully"}

@app.route("/delete/<int:ta_id>", methods=['GET', 'POST'])
@auth.token_auth()
def delete(ta_id):
    existingTA = TA.query.filter(TA.id == ta_id).first()
    db.session.delete(existingTA)
    db.session.commit()
    return {"Success": "TA Deleted Successfully"}

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    token = None

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            token = auth.generate_token(user)
        else:
            return {"Error": "Incorrect password!!!"}

    return jsonify(token)

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return {"Error": "Please Fill up the form"}
    email_exists = User.query.filter_by(email=email).first()

    if email_exists:
        return {"Error": "Email Already Exists!!!"}
    else:
        new_user = User(email=email, password=generate_password_hash(
                password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return {"Success": "User added Successfully"}
