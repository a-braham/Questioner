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
        self.login1 = {
             "username": "Kama",
             "password": "ak?,T4.jj12kjn@"
        }
        self.login2 = {
             "username": "",
             "password": "ak?,T4.jj12kjn@"
        }
        self.login3 = {
             "username": "Kamaa",
             "password": ""
        }
        self.login4 = {
             "username": "Kamaa",
             "password": "hfkhkblllbkjvhcc"
        }

    def test_user_signup(self):
        """ Test signup user """
        response = self.client.post(
            "/api/v1/signup", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["message"], "Username exists")


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

        return self
    def test_get_users(self):
        """ Tests view posted meetups """

        response = self.client.get("/api/v1/get_users", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
    
    def test_user_login(self):
        """ Test login user """

        response = self.client.post(
            "/api/v1/login", data=json.dumps(self.login), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        self.assertTrue(result["token"])

        response1 = self.client.post(
            "/api/v1/login", data=json.dumps(self.login1), content_type="application/json")
        result1 = json.loads(response1.data.decode('utf-8'))

        self.assertEqual(response1.status_code, 404)
        self.assertEqual(result1["status"], 404)
        self.assertEqual(result1["message"], "User does not exist")

        response2 = self.client.post(
            "/api/v1/login", data=json.dumps(self.login2), content_type="application/json")
        result2 = json.loads(response2.data.decode('utf-8'))

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(result2["status"], 400)
        self.assertEqual(result2["message"], "Username is required")

        response3 = self.client.post(
            "/api/v1/login", data=json.dumps(self.login3), content_type="application/json")
        result3 = json.loads(response3.data.decode('utf-8'))

        self.assertEqual(response3.status_code, 400)
        self.assertEqual(result3["status"], 400)
        self.assertEqual(result3["message"], "Password is required")

        response4 = self.client.post(
            "/api/v1/login", data=json.dumps(self.login4), content_type="application/json")
        result4 = json.loads(response4.data.decode('utf-8'))

        self.assertEqual(response4.status_code, 400)
        self.assertEqual(result4["status"], 400)
        self.assertEqual(result4["message"], "Incorrect password")

        #Test User Profile
        response = self.client.get("/api/v1/profile", headers={"Authorization": 'Bearer ' + json.loads(response.data.decode('utf-8'))['token']})
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        

    def tearDown(self):
        """ Method to destroy test client """
        app.testing = False


if __name__ == "__main__":
    unittest.main()
