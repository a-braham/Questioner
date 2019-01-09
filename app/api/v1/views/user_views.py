from flask import Flask, Blueprint, jsonify, request, make_response
from ..models import user_models

user_bp = Blueprint("auth", __name__, url_prefix='/api/v1')
users = user_models.UserModel()

@user_bp.route('/signup', methods=['POST'])
def signup():
    """ A view to control creation of users """
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    othername = data.get('othername')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    isAdmin = data.get('isAdmin')
    password = data.get('password')

    return make_response(jsonify({
        "status": 201,
        "data": [{
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "email": email,
            "phoneNumber": phoneNumber,
            "isAdmin": isAdmin,
            "password": password
        }]
    })), 201

