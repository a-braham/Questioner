from flask import Flask
from instance.config import app_config

def create_app(config_name):
    """ Using the config file in instance folder to create app """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config)

    return app