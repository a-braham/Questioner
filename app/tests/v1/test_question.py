""" Tests for questions endpoints """

import unittest, json, instance
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
            "user": 1,
            "meetup" : 1,
            "title" : "Win32 How to Overlay/Blend 2 windows",
            "body" : "Now I want to be able to draw with the mouse over that window without destroying its content."
        }

    def test_create_question(self):
        """ Method to test creating question """
        
        response = self.client.post("/question", data=json.dumps(self.question), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{
            "user": 1,
            "meetup" : 1,
            "title" : "Win32 How to Overlay/Blend 2 windows",
            "body" : "Now I want to be able to draw with the mouse over that window without destroying its content."
        }])

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False


if __name__ == "__main__":
    unittest.main()