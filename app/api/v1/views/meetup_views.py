""" Views for handling meetup endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from ..models import meetup_models
from werkzeug.exceptions import BadRequest

meetup_bp = Blueprint('meetups', __name__, url_prefix='/meetups')
meetups = meetup_models.MeetUpModel()


@meetup_bp.route('', methods=['POST'])
def create_meetup():
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
    images = data.get('images')
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
        meetup = meetups.create_meetup(
            topic, location, images, happeningOn, tags)
        return make_response(jsonify({
            "status": 201,
            "data": [{"topic": topic,
                      "location": location,
                      "happeningOn": happeningOn,
                      "tags": tags}]})), 201

@meetup_bp.route('', methods=['GET'])
def view_meetups():
    """ A view to get all meetups posted """

    return make_response(jsonify({
        "status": 200,
        "data": meetups.view_meetups()
    })), 200

@meetup_bp.route('/<int:id>', methods=['GET'])
def view_one_meetup(id):
    meetup = meetups.view_one_meetup(id)
    if not meetup:
        return make_response(jsonify({
        "status": 404,
        "message": "Meetup not found"
    })), 404
    return make_response(jsonify({
        "status": 200,
        "data": meetup
    })), 200