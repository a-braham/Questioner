from flask import Flask
from instance.config import app_config
from .api.v1.views import meetup_views, user_views, question_views
from .api.v2.views import user_views as v2_user_views

def create_app(config_name):
    """ Using the config file in instance folder to create app """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config)
    
    app.register_blueprint(meetup_views.meetup_bp)
    app.register_blueprint(user_views.user_bp)
    app.register_blueprint(question_views.question_bp)
    
    # Version 2 blueprints
    app.register_blueprint(v2_user_views.user_bpv2)

    return app