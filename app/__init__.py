from flask import Flask
from instance.config import app_config
from .api.v1.views import meetup_views, user_views

def create_app(config_name):
    """ Using the config file in instance folder to create app """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config)
    
    app.register_blueprint(meetup_views.meetup_bp)
    app.register_blueprint(user_views.user_bp)

    return app