import unittest
import json
import instance
from app.api.v1.views import meetup_views
from app.api.v1.models import meetup_models
from app import create_app

app = create_app("testing")


class TestMeetup(unittest.TestCase):
    """Test class for meetup views """

    def setUp(self):
        """ Method to define test variable """

        app.config.from_object(instance.config.Testing)
        self.client = app.test_client()
        self.meetup = {
            "topic": "Python",
            "location": "Nairobi",
            "images": ["image1.png", "image2.png"],
            "happeningOn": "Thursday",
            "tags": ["RESTful API", "JSON Data"]
        }
        self.meetup1 = {}

    def test_create_meetup(self):
        """ Test creation of meetup """
        response = self.client.post(
            "/meetups", data=json.dumps(self.meetup), content_type="application/json")
        restult = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(restult["status"], 201)
        self.assertEqual(restult["data"], [
            {
                "topic": "Python",
                "location": "Nairobi",
                "happeningOn": "Thursday",
                "tags": ["RESTful API", "JSON Data"],
            }
        ])

        response1 = self.client.post(
            "/meetups", data=json.dumps(self.meetup1), content_type="application/json")
        restult1 = json.loads(response1.data.decode('utf-8'))
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(restult1["status"], 400)
        self.assertEqual(restult1["message"], "Topic cannot be empty")

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False


if __name__ == "__main__":
    unittest.main()
