from flask import Flask, make_response, jsonify
from instance.config import app_config
from .api.v1.views import meetup_views, user_views, question_views

def resource_not_found(message):
    """ Handling resource not found """
    return make_response(jsonify({
        "status": 404,
        "message": str(message)
    }))

def method_not_allow(message):
    """ Handling method not allowed error """

    return make_response(jsonify({
        "status": 405,
        "message": str(message)
    }))

def server_internal_error(message):
    """ Handling internal server error """
    return make_response(jsonify({
        "status": 500,
        "message": str(message)
    }))


def create_app(config_name):
    """ Using the config file in instance folder to create app """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config)
    
    app.register_blueprint(meetup_views.meetup_bp)
    app.register_blueprint(user_views.user_bp)
    app.register_blueprint(question_views.question_bp)

    @app.errorhandler(404)
    def resource_not_found(message):
        """ Handling resource not found """

        return make_response(jsonify({
            "status": 404,
            "message": str(message)
        })), 404

    @app.errorhandler(405)
    def method_not_allowed(message):
        """ Handling method not allowed error """

        return make_response(jsonify({
            "status": 405,
            "message": str(message)
        })), 405

    @app.errorhandler(500)
    def server_internal_error(message):
        """ Handling internal server error """
        return make_response(jsonify({
            "status": 500,
            "message": str(message)
        })), 500

    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, server_internal_error)


    return app