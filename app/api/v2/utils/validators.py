import re
import jwt
from werkzeug.security import check_password_hash
from ..models.user_models import USERS
from app.database import DBOps
from ..models import user_models
from functools import wraps
from flask import request, jsonify, make_response
from instance.config import Config

users = user_models.UserModel()
SECRET_KEY = Config.SECRET_KEY


class UserValidation():
    def __init__(self):
        self.users = DBOps.send_con()

    def validate_password(self, password):
        exp = "^[a-zA-Z0-9@_+-.]{3,}$"
        return re.match(exp, password)

    def validate_email(self, email):
        exp = "^[\w]+[\d]?@[\w]+\.[\w]+$"
        return re.match(exp, email)

    def username_exists(self, username):
        cursor = self.users.cursor()
        cursor.execute(
            """SELECT username FROM users WHERE username = '%s'""" % (username)
        )
        usr = cursor.fetchone()
        if usr:
            return True
        else:
            return False

    def same_password(self, username, password):
        usr = [user for user in self.users if user['username'] == username]
        if usr:
            validate = check_password_hash(usr['password'], password)
            if validate:
                return True
            else:
                return False

    def email_exists(self, email):
        cursor = self.users.cursor()
        cursor.execute(
            """SELECT email FROM users WHERE email = '%s'""" % (email)
        )
        usr = cursor.fetchone()
        if usr:
            return True
        else:
            return False

def requires_auth(func):
    """ validation decorator. Validates if user is logged in before performing a task """
    @wraps(func)
    def decorator_func(*args, **kwargs):
        auth_token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split("Bearer ")[1]
        if not auth_token:
            return make_response(jsonify({
                "status": 401,
                "data": "Unauthorized! Token required"
            })), 401
        try:
            response = users.verify_auth_token(auth_token)
            if isinstance(response, str):
                user = users.login(username=response)[0]
                if not user:
                    return make_response(jsonify({
                        "status": 400,
                        "message": "Authentication failed: Wrong username"
                    })), 400
        except:
            return make_response(jsonify({
                "status": 400,
                "message": "Authentication failed: Invalid token"
            })), 400
<<<<<<< HEAD
        return func(user ,*args, *kwargs)
    decorator_func.__name__ = func.__name__
    return decorator_func

def login_req():
    auth_token = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split("Bearer ")[1]
    if not auth_token:
        return make_response(jsonify({
            "status": 401,
            "data": "Unauthorized! Token required"
        })), 401
    try:
        response = users.verify_auth_token(auth_token)
        if isinstance(response, str):
            user = users.login(username=response)
            return user
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Authentication failed: Invalid token"
        })), 400
=======
        return func(user, *args, *kwargs)
    return decorator_func

def requires_admin(func):
    """ validation decorator. Validates if user is logged and is admin in before performing a task """
    @wraps(func)
    def decorator_func(*args, **kwargs):
        auth_token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split("Bearer ")[1]
        if not auth_token:
            return make_response(jsonify({
                "status": 401,
                "data": "Unauthorized! Token required"
            })), 401
        try:
            response = users.verify_auth_token(auth_token)
            if isinstance(response, str):
                user = users.selectAdmin(username=response)
                if not user:
                    return make_response(jsonify({
                        "status": 400,
                        "message": "Authentication failed: User is not admin"
                    })), 400
        except:
            return make_response(jsonify({
                "status": 400,
                "message": "Authentication failed: Invalid token"
            })), 400
        return func(user, *args, *kwargs)
    return decorator_func
>>>>>>> c8df06f6e0244c74775bfada05d2dcb54dcad7ff
