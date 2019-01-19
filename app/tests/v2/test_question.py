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
        self.vote = {
            "votes": 1
        }
        self.comment = {
            "comment": "This is a comment"
        }
        self.test_DB = _init_db()

    def test_create_question(self):
        """ Method to test creating question """
        self.client.post(
            "/api/v2/signup", data=json.dumps(self.u_register), content_type="application/json"
        )
        user_resp = self.client.post(
            "/api/v2/login", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(user_resp.data.decode('utf-8'))
        token = 'Bearer ' + result["token"]
        header = {"Authorization": token}
        response = self.client.post(
            "api/v2/questions", data=json.dumps(self.question), headers=header, content_type="application/json")
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
        self.client.post(
            "/api/v2/signup", data=json.dumps(self.u_register), content_type="application/json"
        )
        user_resp = self.client.post(
            "/api/v2/login", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(user_resp.data.decode('utf-8'))
        token = 'Bearer ' + result["token"]
        header = {"Authorization": token}
        self.client.post("/api/v2/questions", data=json.dumps(self.question), content_type="application/json")
        response = self.client.patch("/api/v2/questions/1/upvote", data=json.dumps(self.vote), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

    def test_downvote(self):
        """ Testing downvoting endpoint """
        self.client.post(
            "/api/v2/signup", data=json.dumps(self.u_register), content_type="application/json"
        )
        user_resp = self.client.post(
            "/api/v2/login", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(user_resp.data.decode('utf-8'))
        token = 'Bearer ' + result["token"]
        header = {"Authorization": token}
        self.client.post("/api/v2/questions", data=json.dumps(self.question), content_type="application/json")
        response = self.client.patch("/api/v2/questions/1/downvote", data=json.dumps(self.vote), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

    def test_comments(self):
        """ Test run to test comments endpoints """
        self.client.post(
            "/api/v2/signup", data=json.dumps(self.u_register), content_type="application/json"
        )
        user_resp = self.client.post(
            "/api/v2/login", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(user_resp.data.decode('utf-8'))
        token = 'Bearer ' + result["token"]
        header = {"Authorization": token}
        self.client.post("api/v2/questions", data=json.dumps(self.question), content_type="application/json")
        response = self.client.post("api/v2/questions/1/comment", data=json.dumps(self.comment), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False
        destroy_db()
        self.test_DB.close()


if __name__ == "__main__":
    unittest.main()
