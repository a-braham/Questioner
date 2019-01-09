""" Views for handling quetion endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from ..models import question_models
from werkzeug.exceptions import BadRequest

question_bp = Blueprint('questions', __name__, url_prefix='/api/v1/questions')
questions = question_models.QuestionModel()


@question_bp.route('', methods=['POST'])
def create_question():
    """ A view to control creation of question """

    data = request.get_json()

    title = data.get('title')
    body = data.get('body')
    meetup = data.get('meetup')
    createdby = data.get('createdby')
    votes = data.get('votes')

    return make_response(jsonify({
        "status": 201,
        "data": [{
            "title": title,
            "body": body,
            "meetup": meetup,
            "createdby": createdby,
            "votes": votes
        }]})), 201
