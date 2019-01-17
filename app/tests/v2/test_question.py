""" Tests for questions endpoints """

import unittest
import json
import instance
from app.api.v1.views import question_views
from app.api.v1.models import question_models
from app import create_app
from app.database import _init_db, destroy_db

app = create_app("testing")


class TestQuestion(unittest.TestCase):
    """ Test class to test Questions """

    def setUp(self):
        """ Define test variable """

        app.config.from_object(instance.config.Testing)
        self.client = app.test_client()
        self.question = {
            "title": "Man",
            "body": "Not Hot",
            "meetup": 1,
            "createdby": 1,
            "votes": 0
        }
        self.vote = {
            "votes": 1
        }
        self.test_DB = _init_db()

    def test_create_question(self):
        """ Method to test creating question """

        response = self.client.post(
            "api/v2/questions", data=json.dumps(self.question), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{
            "body": "Not Hot",
            "user": 1,
            "meetup": 1,
            "title": "Man"
        }])

    def test_upvote(self):
        """ Testing upvoting endpoint """

        self.client.post("/api/v2/questions", data=json.dumps(self.question), content_type="application/json")
        response = self.client.patch("/api/v2/questions/1/upvote", data=json.dumps(self.vote), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

    def test_downvote(self):
        """ Testing downvoting endpoint """

        self.client.post("/api/v2/questions", data=json.dumps(self.question), content_type="application/json")
        response = self.client.patch("/api/v2/questions/1/downvote", data=json.dumps(self.vote), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False
        destroy_db()
        self.test_DB.close()


if __name__ == "__main__":
    unittest.main()
