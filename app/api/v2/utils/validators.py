import re
import jwt
from werkzeug.security import check_password_hash
from app.database import DBOps
from ..models import user_models
from functools import wraps
from flask import request, jsonify, make_response
from instance.config import Config
from datetime import datetime

users = user_models.UserModel()
SECRET_KEY = Config.SECRET_KEY


class UserValidation():
    def __init__(self):
        self.users = DBOps.send_con()

    def validate_password(self, password):
        special=['$','@','#']
        valid=True
        if len(password) < 6:
            valid=False
        if len(password) > 12:
            valid=False
        if not any(char.isdigit() for char in password):
            valid=False
        if not any(char.isupper() for char in password):
            valid=False
        if not any(char.islower() for char in password):
            valid=False
        if not any(char in special for char in password):
            valid=False
        if valid:
            pass
        return valid

    def validate_email(self, email):
        exp = "^[\w]+[\d]?@[\w]+\.[\w]+$"
        return re.match(exp, email)
    
    def validate_date(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format")

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

def requires_admin(func):
    """ validation decorator. Validates if user is logged in is admin"""
    @wraps(func)
    def decorator_func(*args, **kwargs):
        auth_token = None
        if 'Authorization' in request.headers:
            auth_token = request.headers['Authorization']
        if not auth_token:
            return jsonify({
                "status": 401,
                "error": "missing token"
                }), 401
        try:
            response = users.verify_auth_token(auth_token)
            if isinstance(response, str):
                user = users.selectAdmin(username=response)
                if not user:
                    return make_response(jsonify({
                        "status": 400,
                        "message": "Authentication failed: User is not admin"
                    })), 400
        except Exception as e:
            return jsonify({
                "status": 401,
                "error": "The token is invalid! " + str(e),
            }), 401
        return func(user, *args, **kwargs)
    return decorator_func

def requires_auth(func):
    """ validation decorator. Validates if user is logged in before performing a task """
    @wraps(func)
    def decorator_func(*args, **kwargs):
        auth_token = None
        if 'Authorization' in request.headers:
            auth_token = request.headers['Authorization']
        if not auth_token:
            return jsonify({
                "status": 401,
                "message": "missing token"
                }), 401
        try:
            response = users.verify_auth_token(auth_token)
            if isinstance(response, str):
                user = users.login(username=response)[0]
                if not user:
                    return make_response(jsonify({
                        "status": 400,
                        "message": "Authentication failed: Wrong username"
                    })), 400
        except Exception as e:
            return jsonify({
                "status": 401,
                "message": "Invalid token, Login! "
            }), 401
        return func(user, *args, **kwargs)
    return decorator_func
