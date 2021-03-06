from flask import Flask, make_response, jsonify
from flask_cors import CORS
from instance.config import app_config
from .database import DBOps

def create_app(config_name):
    """ Using the config file in instance folder to create app """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    with app.app_context():
        DBOps.connect_to(app.config["DATABASE_URI"])
        DBOps.init_db()
        DBOps.create_admin()
    
    # Version 1 blueprints
    from .api.v1.views import meetup_views, user_views, question_views
    app.register_blueprint(meetup_views.meetup_bp)
    app.register_blueprint(user_views.user_bp)
    app.register_blueprint(question_views.question_bp)
    
    # Version 2 blueprints
    from .api.v2.views import user_views, meetup_views, question_views
    app.register_blueprint(user_views.user_bpv2)
    app.register_blueprint(meetup_views.meetup_bpv2)
    app.register_blueprint(question_views.question_bpv2)

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
