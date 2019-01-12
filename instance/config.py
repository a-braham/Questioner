import os

class Config(object):
    """ Main configurations class """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret')

class Development(Config):
    """ Development configurations are put here """
    DEBUG = True

class Testing(Config):
    """ The configurations for testing """
    DEBUG = True
    TESTING = True

class Production(Config):
    """ The configurations for production """
    DEBUG = False
    TESTING = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}