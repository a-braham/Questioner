""" Views for handling meetup endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from datetime import datetime
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
    description = data.get('description')
    location = data.get('location')
    happeningOn = data.get('happeningOn')

    if not topic.strip():
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
    if happeningOn < datetime.now().strftime("%Y-%m-%d"):
        return make_response(jsonify({
            "status": 400,
            "message": "Date cannot be in the past"
        })), 400
    if validate.validate_meetup(topic, location, happeningOn):
        return make_response(jsonify({
            "status": 400,
            "message": "Another meetup with the same topic, location and date exists"
        })), 400
    else:
        meetups.create_meetup(
            topic, description, location, happeningOn)
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
    rsvp_exist = meetups.search_rsvp(meetup_id, user)
    if rsvp_exist:
        meetups.update_rsvp(rsvp_data, meetup_id, user)
        return make_response(jsonify({
            "status": 200,
            "message": "RSVP set!"
            })), 200
    if meetup:
        rsvp=meetups.create_rsvps(rsvp_data, meetup_id, user)
        return make_response(jsonify({
            "status": 201,
            "message": "RSVP set!"
            })), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Meetup not found"
    })), 404

@meetup_bpv2.route('/<int:meetup_id>/rsvps_count', methods=['GET'])
def count_rsvps(meetup_id):
    """ A view to get rsvps count """

    return make_response(jsonify({
        "status": 200,
        "data": meetups.count_rsvp(meetup_id)
    })), 200

@meetup_bpv2.route('/<int:meetup_id>/tags', methods=['POST'])
@requires_admin
def tags(user, meetup_id):
    """ A method for sending rsvps """
    meetup = meetups.view_one_meetup(meetup_id)
    data = request.get_json()
    tag_data = data.get('tags')
    if meetup:
        tag=meetups.create_tags(tag_data, meetup_id)
        return make_response(jsonify({
            "status": 201,
            "data": tag
            })), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Meetup not found"
    })), 404


@meetup_bpv2.route('/<int:meetup_id>/delete', methods=['DELETE'])
@requires_admin
def meetup_delete(user, meetup_id):
    """ A method for sending rsvps """
    meetup = meetups.view_one_meetup(meetup_id)
    if meetup:
        delet = meetups.delete_meetup(meetup_id)
        return make_response(jsonify({
            "status": 201,
            "message": delet
            })), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Meetup not found"
    })), 404
