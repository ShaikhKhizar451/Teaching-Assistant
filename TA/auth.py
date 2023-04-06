from flask import request
import re
import jwt
from .models import User
from functools import wraps
from datetime import datetime, timedelta


def token_auth():
    def inner1(func):
        @wraps(func)
        def inner2(**args):
            authorization = request.headers.get("authorization")
            if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                token = authorization.split(" ")[1]
                try:
                    jwtdecode = jwt.decode(token, "Khizar", algorithms="HS256")
                except jwt.ExpiredSignatureError:
                    return {"Error": "TOKEN EXPIRED"}
                except jwt.exceptions.InvalidSignatureError:
                    return {"ERROR": "INVALID USER"}
                user = User.query.filter_by(email=jwtdecode['payload']['email']).first()
                if user:
                    return func(**args)
                else:
                    return {"ERROR": "INVALID USER"}
            else:
                return "Something went wrong"
        return inner2
    return inner1


def generate_token(user):
    userdata = {"id": user.id, "email": user.email}
    exp_time = datetime.now() + timedelta(minutes=15)
    exp_epoch_time = int(exp_time.timestamp())
    payload = {
        "payload": userdata,
        "exp": exp_epoch_time
    }
    token = jwt.encode(payload, "Khizar", algorithm="HS256")
    return token
