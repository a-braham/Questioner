""" Views for handling quetion endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from ..models import question_models
from werkzeug.exceptions import BadRequest

question_bpv2 = Blueprint('questionsv2', __name__,
                          url_prefix='/api/v2/questions')
questions = question_models.QuestionModel()


@question_bpv2.route('', methods=['POST'])
def create_question():
    """ A view to control creation of question """

    try:
        data = request.get_json()
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong input"
        })), 400

    title = data.get('title')
    body = data.get('body')
    meetup = data.get('meetup')
    createdby = data.get('createdby')
    votes = data.get('votes')

    if not title:
        return make_response(jsonify({
            "status": 400,
            "message": "Title cannot be empty"
        })), 400

    if not body:
        return make_response(jsonify({
            "status": 400,
            "message": "Body cannot be empty"
        })), 400
    questions.create_question(
        title, body, meetup, createdby, votes)
    return make_response(jsonify({
        "status": 201,
        "data": [{
            "title": title,
            "body": body,
            "meetup": meetup,
            "user": createdby,
        }]})), 201


@question_bpv2.route('/<int:question_id>/upvote', methods=['PATCH'])
def upvote(question_id):
    """ Manipulates upvoting question """

    question = questions.oneQuestion(question_id)
    if question:
        quiz = question[0]
        quiz["votes"] = quiz["votes"] + 1
        return make_response(jsonify({
            "status": 200,
            "data": quiz
        })), 200
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    })), 404


@question_bpv2.route('/<int:question_id>/downvote', methods=['PATCH'])
def downvote(question_id):
    """ Manipulates upvoting question """

    question = questions.oneQuestion(question_id)
    if question:
        quiz = question[0]
        quiz["votes"] = quiz["votes"] - 1
        return make_response(jsonify({
            "status": 200,
            "data": quiz
        })), 200
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    })), 404


@question_bpv2.route('/<int:question_id>/comment', methods=['POST'])
def comments(question_id):
    """A method to enable posting of comments based on user question """
    question = questions.oneQuestion(question_id)
    if question:
        try:
            data = request.get_json()
        except Exception as e:
            return make_response(jsonify({
                "status": 400,
                "message": "Invalid or no data sent" + e
            }))
        comment = data.get("comment")
        if not comment:
            return make_response(jsonify({
                "status": 400,
                "message": "Comment posted is empty"
            }))
        questions.create_comment(question_id, comment)
        return make_response(jsonify({
            "status": 201,
            "data": [{
                "question": question_id,
                "comment": comment
            }]
        })), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    }))