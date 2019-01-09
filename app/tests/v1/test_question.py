""" Tests for questions endpoints """

import unittest
import json
import instance
from app.api.v1.views import question_views
from app.api.v1.models import question_models
from app import create_app

app = create_app("testing")


class TestQuestion(unittest.TestCase):
    """ Test class to test Questions """

    def setUp(self):
        """ Define test variable """

        app.config.from_object(instance.config.Testing)
        self.client = app.test_client()
        self.question = {
            "title": "title",
            "body": "body",
            "meetup": "meetup",
            "createdby": "createdby",
            "votes": "votes"
        }

    def test_create_question(self):
        """ Method to test creating question """

        response = self.client.post(
            "api/v1/questions", data=json.dumps(self.question), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{
            "body": "body",
            "createdby": "createdby",
            "meetup": "meetup",
            "title": "title",
            "votes": "votes"
        }])

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False


if __name__ == "__main__":
    unittest.main()
