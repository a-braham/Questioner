""" Test for User endpoints """

import unittest
import json
import instance
from app.api.v1.views import user_views
from app.api.v1.models import user_models
from app import create_app

app = create_app("testing")


class TestUser(unittest.TestCase):
    """ Test class for user endpoints """

    def setUp(self):
        """ Defining test variables """

        app.config.from_object(instance.config.Testing)
        self.client = app.test_client()
        self.user = {
             "firstname": "Django",
             "lastname": "Nairobi",
             "othername": "wsjdkhkvk",
             "email": "Thursday",
             "phoneNumber": "123456789",
             "isAdmin": "Django",
             "password": "Nairobi"
        }

    def test_user_signup(self):
        """ Test signup user """

        response = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        # self.assertEqual(result["data"], [{}])

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False


if __name__ == "__main__":
    unittest.main()
