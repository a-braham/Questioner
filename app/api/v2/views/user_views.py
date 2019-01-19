from flask import Flask, Blueprint, jsonify, request, make_response
from ..models import user_models
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.validators import UserValidation, requires_auth

user_bpv2 = Blueprint("authv2", __name__, url_prefix='/api/v2')
users = user_models.UserModel()
validator = UserValidation()


@user_bpv2.route('/signup', methods=['POST'])
def signup():
    """ A view to control creation of users """

    try:
        data = request.get_json()
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong input"
        })), 400

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    othername = data.get('othername')
    email = data.get('email')
    phone = data.get('phoneNumber')
    username = data.get('username')
    password = data.get('password')

    if not firstname:
        return make_response(jsonify({
            "status": 400,
            "message": "Firstname is required"
        })), 400
    if not lastname:
        return make_response(jsonify({
            "status": 400,
            "message": "Lastname is required"
        })), 400
    if not email:
        return make_response(jsonify({
            "status": 400,
            "message": "email is required"
        })), 400
    if not phone:
        return make_response(jsonify({
            "status": 400,
            "message": "Phonenumber is required"
        })), 400
    if not username:
        return make_response(jsonify({
            "status": 400,
            "message": "Username is required"
        })), 400
    if not password:
        return make_response(jsonify({
            "status": 400,
            "message": "Password is required"
        })), 400

    if validator.validate_password(password):
        return make_response(jsonify({
            "status": 400,
            "message": "Password not valid"
        })), 400

    if not validator.validate_email(email):
        return make_response(jsonify({
            "status": 400,
            "message": "Invalid email"
        })), 400

    if validator.username_exists(username):
        return make_response(jsonify({
            "status": 400,
            "message": "Username exists"
        })), 400

    if validator.email_exists(email):
        return make_response(jsonify({
            "status": 400,
            "message": "Email exists"
        })), 400

    password = generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=8)

    # new_user = {}

    # for key in data:
    #     new_user[key] = data[key]

    # new_user["isAdmin"] = False

    user = users.signup(
        firstname, lastname, othername, email, phone, username, password)
    return make_response(jsonify({
        "status": 201,
        "data": [{
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "email": email,
            "phoneNumber": phone,
            "username": username,
        }]
    })), 201


@user_bpv2.route('/login', methods=['POST'])
def login():
    """ A view to control users login """
    try:
        data = request.get_json()
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong input"
        })), 400
    username = data.get('username')
    password = data.get('password')

    if not username:
        return make_response(jsonify({
            "status": 400,
            "message": "Username is required"
        })), 400
    if not password:
        return make_response(jsonify({
            "status": 400,
            "message": "Password is required"
        })), 400
    user = users.login(username)
    if user:
        if check_password_hash(user[1], password):
            auth_token = users.generate_auth_token(username)
            return make_response(jsonify({
                "status": 200,
                "token": auth_token
            })), 200
        return make_response(jsonify({
            "status": 400,
            "message": "Incorrect password"
        })), 400
    return make_response(jsonify({
        "status": 404,
        "message": "User does not exist"
    })), 404


@user_bpv2.route('/get_users', methods=['GET'])
def get_users():
    """ A method to get all users posted """
    usrs = users.get_users()
    if usrs:
        return make_response(jsonify({
            "status": 200,
            "data": [{
                "firstname": [usr[1] for usr in usrs],
                "lastname": [usr[2] for usr in usrs],
                "othername": [usr[3] for usr in usrs],
                "username": [usr[4] for usr in usrs],
                "phoneNumber": [usr[6] for usr in usrs],
                "email": [usr[5] for usr in usrs],
                "isAdmin": [usr[7] for usr in usrs],
            }]}))
    return make_response(jsonify({
        "status": 404,
        "message": "There are no users"
    })), 404


@user_bpv2.route('/profile', methods=['GET'])
def profile():
    """ Method to get logged in user """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split("Bearer ")[1]
    else:
        auth_token = 'Bearer '
    if auth_token:
        response = users.verify_auth_token(auth_token)
        if isinstance(response, str):
            user = users.login(username=response)
            if not user:
                return make_response(jsonify({
                    "status": 400,
                    "message": "Authentication failed"
                })), 400
            return make_response(jsonify({
                "status": 200,
                "data": user
            })), 200
        return make_response(jsonify({
            "status": 400,
            "message": "Authentication token failed"
        })), 400
    return make_response(jsonify({
        "status": 404,
        "data": "Token not found"
    })), 404
