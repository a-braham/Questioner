""" Views for handling meetup endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from ..models import meetup_models
from ..models import user_models
from werkzeug.exceptions import BadRequest
from ..utils.validators import requires_auth, requires_admin, UserValidation

meetup_bpv2 = Blueprint('meetupsv2', __name__, url_prefix='/api/v2/meetups')
meetups = meetup_models.MeetUpModel()
users = user_models.UserModel()

@meetup_bpv2.route('', methods=['POST'])
@requires_admin
def create_meetup(func):
    """ A view to control creation of meetups """

    try:
        data = request.get_json()
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong input"
        })), 400
    topic = data.get('topic')
    location = data.get('location')
    happeningOn = data.get('happeningOn')

    if not topic:
        return make_response(jsonify({
            "status": 400,
            "message": "Topic cannot be empty"
        })), 400
    if not location:
        return make_response(jsonify({
            "status": 400,
            "message": "Location cannot be empty"
        })), 400
    if not happeningOn:
        return make_response(jsonify({
            "status": 400,
            "message": "Meetup Date cannot be empty"
        })), 400
    validate = UserValidation()
    if validate.validate_date(happeningOn):
        return make_response(jsonify({
            "status": 400,
            "message": "Use correct date time format"
        })), 400
    else:
        meetups.create_meetup(
            topic, location, happeningOn)
        return make_response(jsonify({
            "status": 201,
            "data": [{"topic": topic,
                      "location": location,
                      "happeningOn": happeningOn}]})), 201


@meetup_bpv2.route('/upcoming', methods=['GET'])
def view_meetups():
    """ A view to get all meetups posted """

    return make_response(jsonify({
        "status": 200,
        "data": meetups.view_meetups()
    })), 200


@meetup_bpv2.route('/<int:mid>', methods=['GET'])
def view_one_meetup(mid):
    meetup = meetups.view_one_meetup(mid)
    if not meetup:
        return make_response(jsonify({
            "status": 404,
            "message": "Meetup not found"
        })), 404
    return make_response(jsonify({
        "status": 200,
        "data": meetup
    })), 200


@meetup_bpv2.route('/<int:meetup_id>/rsvps', methods=['POST'])
@requires_auth
def rsvps(user, meetup_id):
    """ A method for sending rsvps """
    rsvps_data = ["yes", "no", "maybe"]
    meetup = meetups.view_one_meetup(meetup_id)
    user = users.login(user)[2]
    data = request.get_json()
    rsvp_data = data.get('rsvp')
    if rsvp_data not in rsvps_data:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong imput: Enter either --yes--, --no--, --maybe--"
        })), 400
    if meetup:
        rsvp=meetups.create_rsvps(rsvp_data, meetup_id, user)
        return make_response(jsonify({
            "status": 201,
            "data": rsvp
            })), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Meetup not found"
    })), 404


@meetup_bpv2.route('/<int:meetup_id>/delete', methods=['DELETE'])
@requires_admin
def meetup_delete(user, meetup_id):
    """ A method for sending rsvps """
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
            meetup = meetups.view_one_meetup(meetup_id)
            if meetup:
                meetups.delete_meetup(meetup_id)
                return make_response(jsonify({
                    "status": 201,
                    "message": "Meetup deleted!!:"
                    })), 201
            return make_response(jsonify({
                "status": 404,
                "message": "Meetup not found"
            })), 404
        return make_response(jsonify({
            "status": 400,
            "message": "Authentication token failed"
        })), 400
    return make_response(jsonify({
        "status": 404,
        "data": "Token not found"
    })), 404
