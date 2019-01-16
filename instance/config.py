import os

class Config(object):
    """ Main configurations class """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret')
    DATABASE_URL = os.getenv('DATABASE_URL')

class Development(Config):
    """ Development configurations are put here """
    DEBUG = True

class Testing(Config):
    """ The configurations for testing """
    DEBUG = True
    TESTING = True
    DATABASE_TEST_URL = os.getenv('DATABASE_TEST_URL')

class Production(Config):
    """ The configurations for production """
    DEBUG = False
    TESTING = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}