import unittest
from flask import current_app, Flask
import instance

app = Flask(__name__, instance_relative_config=True)

class TestDevelopmentConfig(unittest.TestCase):
    """ Test for Development Config """
    
    def create_app(self):
        app.config.from_object('instance.config.DevelopmentConfig')
        return app

    def test_development_config(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)

class TestTestingConfig(unittest.TestCase):
    """ Test for Testing Config """

    def create_app(self):
        app.config.from_object('instance.config.TestingConfig')
        return app

    def test_testing_config(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'] is True)

class TestProductionConfig(unittest.TestCase):
    """ Test for Production Config """

    def create_app(self):
        app.config.from_object('instance.config.ProductionConfig')
        return app

    def test_production_config(self):
        self.assertTrue(app.config['DEBUG'] is False)

if __name__ == "__main__":
    unittest.main()