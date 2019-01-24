""" Views for handling quetion endpoints """

from flask import Flask, Blueprint, request, make_response, jsonify
from ..models import question_models, user_models, meetup_models
from werkzeug.exceptions import BadRequest
from ..utils.validators import requires_auth, requires_admin

question_bpv2 = Blueprint('questionsv2', __name__,
                          url_prefix='/api/v2/questions')
questions = question_models.QuestionModel()
users = user_models.UserModel()
meetups = meetup_models.MeetUpModel()

@question_bpv2.route('meetup/<int:meetup_id>', methods=['POST'])
@requires_auth
def create_question(user, meetup_id):
    """ A view to control creation of question """
    user = users.login(user)[2]
    meetup = meetups.view_one_meetup(meetup_id)[0]
    if not meetup:
        return make_response(jsonify({
            "status": 404,
            "message": "Meetup not found"
        })), 404
    try:
        data = request.get_json()
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong input"
        })), 400

    title = data.get('title')
    body = data.get('body')
    meetup = meetup
    createdby = user
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


@question_bpv2.route('/<int:question_id>', methods=['GET'])
def question(question_id):
    """ Manipulates upvoting question """
    questionz = questions.oneQuestion(question_id)
    if questionz:
        quiz = [question for question in questionz]
        return make_response(jsonify({
            "status": 200,
            "data": quiz
        })), 200
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    })), 404


@question_bpv2.route('/<int:question_id>/upvote', methods=['PATCH'])
@requires_auth
def upvote(user, question_id):
    """ Manipulates upvoting question """
    questionz = questions.oneQuestion(question_id)
    user = users.login(user)[2]
    if questionz:
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "status": 400,
                "message": "Wrong input"
            })), 400
        vote = int(data.get('votes'))
        if vote not in [1]:
            return make_response(jsonify({
                "status": 400,
                "message": "Vote not allowed"
            })), 400
        usr = questions.get_voted_up(user)
        if not usr:
            votes = questions.upVote(question_id, user, vote)
            return make_response(jsonify({
                "status": 200,
                "data": votes
            })), 200
        return make_response(jsonify({
            "status": 400,
            "message": "Not allowed to vote again"
        })), 400
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    })), 404

@question_bpv2.route('/<int:question_id>/downvote', methods=['PATCH'])
@requires_auth
def downvote(user, question_id):
    """ Manipulates upvoting question """
    questionz = questions.oneQuestion(int(question_id))
    user = users.login(user)[2]
    if questionz:
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "status": 400,
                "message": "Wrong input"
            })), 400
        vote = int(data.get('votes'))
        if vote not in [1]:
            return make_response(jsonify({
                "status": 400,
                "message": "Vote not allowed"
            })), 400
        usr = questions.get_voted_down(user)
        if not usr:
            votes = questions.downVote(question_id, user, vote)
            return make_response(jsonify({
                "status": 200,
                "data": votes
            })), 200
        return make_response(jsonify({
            "status": 400,
            "message": "Not allowed to vote again"
        })), 400
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    })), 404

@question_bpv2.route('/<int:q_id>/comment', methods=['POST'])
@requires_auth
def comments(user, q_id):
    """A method to enable posting of comments based on user question """
    question = questions.oneQuestion(q_id)[0]
    user = users.login(user)[2]
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
        questions.create_comment(q_id, comment, user)
        return make_response(jsonify({
            "status": 201,
            "data": [{
                "question": q_id,
                "comment": comment
            }]
        })), 201
    return make_response(jsonify({
        "status": 404,
        "message": "Question not found"
    }))
  
