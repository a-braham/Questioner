import unittest, token
import json
import instance
from app.api.v1.views import meetup_views
from app.api.v1.models import meetup_models, user_models
from app import create_app
from app.database import _init_db, destroy_db

app = create_app("testing")
users = user_models.UserModel()

class TestMeetup(unittest.TestCase):
    """Test class for meetup views """

    def setUp(self):
        """ Method to define test variable """

        app.config.from_object(instance.config.Testing)
        self.client = app.test_client()
        self.meetup = {
            "topic": "Python",
            "location": "Nairobi",
            "happeningOn": "2019-01-17 04:37:40",
            "tags": ["RESTful API", "JSON Data"]
        }
        self.meetup1 = {}

        self.rsvp = {
            "rsvp": "yes",
        }

        self.u_register = {
             "firstname": "Abraham",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "eric@gmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }

        self.user = {
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }
        self.test_DB = _init_db()

    def test_create_meetup(self):
        """ Test creation of meetup """
        user = users.login(self.user["username"])
        if not user:
            response = self.client.post(
                "/api/v2/signup", data=json.dumps(self.user), content_type="application/json"
            )
        user = self.client.post(
            "/api/v2/login", data=json.dumps(self.user), content_type="application/json")
        response = self.client.post(
            "/api/v2/meetups", 
            headers={"Authorization": 'Bearer ' + json.loads(user.data.decode('utf-8'))['token']}, 
            data=json.dumps(self.meetup), content_type="application/json")
        restult = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(restult["status"], 201)
        self.assertEqual(restult["data"], [
            {
                "topic": "Python",
                "location": "Nairobi",
                "happeningOn": "2019-01-17 04:37:40",
                "tags": ["RESTful API", "JSON Data"],
            }
        ])

        response1 = self.client.post(
            "/api/v2/meetups", 
            headers={"Authorization": 'Bearer ' + json.loads(user.data.decode('utf-8'))['token']}, 
            data=json.dumps(self.meetup1), content_type="application/json")
        restult1 = json.loads(response1.data.decode('utf-8'))
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(restult1["status"], 400)
        self.assertEqual(restult1["message"], "Topic cannot be empty")

    def test_view_meetup(self):
        """ Tests view posted meetups """

        self.client.post("/api/v1/meetups", data=json.dumps(self.meetup), content_type="application/json")
        response = self.client.get("/api/v1/meetups/upcoming", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        # self.assertEqual(result["data"], [
        #     {
        #         "topic": "Python",
        #         "location": "Nairobi",
        #         "happeningOn": "Thursday",
        #         "tags": ["RESTful API", "JSON Data"],
        #     }
        # ])
    def test_view_one_meetup(self):
        """ Tests view posted meetups """

        self.client.post("/api/v1/meetups", data=json.dumps(self.meetup), content_type="application/json")
        response = self.client.get("/api/v1/meetups/1", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

    def test_create_rsvp(self):
        """ Tests view posted meetups """

        self.client.post("/api/v2/meetups", data=json.dumps(self.meetup), content_type="application/json")
        response = self.client.post("/api/v2/meetups/1/rsvps", data=json.dumps(self.rsvp), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [
            {
                "meetup": 1,
                "topic": "Python",
                "status": "yes",
            }
        ])


    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False
        destroy_db()
        self.test_DB.close()


if __name__ == "__main__":
    unittest.main()
