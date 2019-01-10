from flask import Flask, Blueprint, jsonify, request, make_response
from ..models import user_models
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.validators import UserValidation

user_bp = Blueprint("auth", __name__, url_prefix='/api/v1')
users = user_models.UserModel()
validator = UserValidation()


@user_bp.route('/signup', methods=['POST'])
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
    phoneNumber = data.get('phoneNumber')
    username = data.get('username')
    isAdmin = data.get('isAdmin')
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
    if not phoneNumber:
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

    return make_response(jsonify({
        "status": 201,
        "data": [{
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "email": email,
            "phoneNumber": phoneNumber,
            "username": username,
            "isAdmin": isAdmin,
        }]
    })), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """ A view to control users login """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if len(username) == 0 or len(password) == 0:
        return make_response(jsonify({
            "status": 400,
            "message": "Email or password is missing"
        })), 400
    if len(username) == 0 and len(password) == 0:
        response = {
            "status": 404,
            "message": "User does not exist."
        }
        return make_response(jsonify(response)), 404
    else:
        response = {
            "status": 200,
            "message": "Login successful!",
            "username": username
        }
        return make_response(jsonify(response)), 200