""" Views for handling meetup endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from ..models import meetup_models
from werkzeug.exceptions import BadRequest
from ..utils.validators import requires_auth, requires_admin

meetup_bpv2 = Blueprint('meetupsv2', __name__, url_prefix='/api/v2/meetups')
meetups = meetup_models.MeetUpModel()


@meetup_bpv2.route('', methods=['POST'])
@requires_auth
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
    tags = data.get('tags')

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
    if not tags:
        return make_response(jsonify({
            "status": 400,
            "message": "Tags cannot be empty"
        })), 400
    else:
        meetups.create_meetup(
            topic, location, happeningOn, tags)
        return make_response(jsonify({
            "status": 201,
            "data": [{"topic": topic,
                      "location": location,
                      "happeningOn": happeningOn,
                      "tags": tags}]})), 201


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
def rsvps(meetup_id):
    """ A method for sending rsvps """
    rsvps_data = ["yes", "no", "maybe"]
    meetup = meetups.view_one_meetup(meetup_id)

    data = request.get_json()
    rsvp_data = data.get('rsvp')
    if rsvp_data not in rsvps_data:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong imput: Enter either --yes--, --no--, --maybe--"
        })), 400
    if meetup:
        meetup = meetup[0]
        meetups.create_rsvps(rsvp_data, meetup_id)
        return make_response(jsonify({
            "status": 201,
            "data": [{
                "meetup": meetup["id"],
                "topic": meetup["topic"],
                "status": rsvp_data
            }]})), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Meetup not found"
    })), 404
