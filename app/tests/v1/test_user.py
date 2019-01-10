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
             "firstname": "Abraham",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "eric@gmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }
        self.user1 = {
             "firstname": "Abraham",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "eric@gmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "qwerty"
        }
        self.user2 = {
             "firstname": "Abraham",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "ericgmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }
        self.user3 = {
             "firstname": "",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "ericgmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }
        self.user4 = {
             "firstname": "Abraham",
             "lastname": "",
             "othername": "Kamau",
             "email": "ericgmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }
        self.user5 = {
             "firstname": "Abraham",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }
        self.user6 = {
             "firstname": "Abraham",
             "lastname": "Kirumba",
             "othername": "Kamau",
             "email": "ericgmail.com",
             "phoneNumber": "123456789",
             "isAdmin": "True",
             "username": "Kamaa",
             "password": ""
        }

        self.login = {
             "username": "Kamaa",
             "password": "ak?,T4.jj12kjn@"
        }

    def test_user_signup(self):
        """ Test signup user """

        response = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{
            "email": "eric@gmail.com",
            "firstname": "Abraham",
            "isAdmin": "True",
            "lastname": "Kirumba",
            "othername": "Kamau",
            "phoneNumber": "123456789",
            "username": "Kamaa"
        }])

        response1 = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user1), content_type="application/json")
        result1 = json.loads(response1.data.decode('utf-8'))

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(result1["status"], 400)
        self.assertEqual(result1["message"], "Password not valid")

        response2 = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user2), content_type="application/json")
        result2 = json.loads(response2.data.decode('utf-8'))

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(result2["status"], 400)
        self.assertEqual(result2["message"], "Invalid email")

        response3 = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user3), content_type="application/json")
        result3 = json.loads(response3.data.decode('utf-8'))

        self.assertEqual(response3.status_code, 400)
        self.assertEqual(result3["status"], 400)
        self.assertEqual(result3["message"], "Firstname is required")

        response4 = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user4), content_type="application/json")
        result4 = json.loads(response4.data.decode('utf-8'))

        self.assertEqual(response4.status_code, 400)
        self.assertEqual(result4["status"], 400)
        self.assertEqual(result4["message"], "Lastname is required")

        response5 = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user5), content_type="application/json")
        result5 = json.loads(response5.data.decode('utf-8'))

        self.assertEqual(response5.status_code, 400)
        self.assertEqual(result5["status"], 400)
        self.assertEqual(result5["message"], "email is required")

        response6 = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user6), content_type="application/json")
        result6 = json.loads(response6.data.decode('utf-8'))

        self.assertEqual(response6.status_code, 400)
        self.assertEqual(result6["status"], 400)
        self.assertEqual(result6["message"], "Password is required")

    def test_user_login(self):
        """ Test login user """

        register = self.client.post("/api/v1/signup", data=json.dumps(self.user), content_type="application/json")
        register_data = json.loads(register.data.decode('utf-8'))
        self.assertEqual(register.status_code, 201)
        self.assertEqual(register_data["status"], 201)

        response = self.client.post(
            "/api/v1/login", data=json.dumps(self.login), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["data"], [{
            "username": "Kamaa"
        }])

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False


if __name__ == "__main__":
    unittest.main()
