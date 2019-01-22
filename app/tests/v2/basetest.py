import unittest
import json
from app import create_app
from app.database import DBOps


class BaseTest(unittest.TestCase):
    """ Test class for user endpoints """

    def setUp(self):
        """ Defining test variables """

        app = create_app("testing")
        self.client = app.test_client()
        self.client.testing = True

        self.user = {
            "firstname": "Abraham",
            "lastname": "Kirumba",
            "othername": "Kamau",
            "email": "eric@gmail.com",
            "isAdmin": "True",
            "username": "Kamaa",
            "phoneNumber": "123456789",
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
        self.user7 = {
            "firstname": "Abraham",
            "lastname": "Kirumba",
            "othername": "Kamau",
            "email": "eric@gmail.com",
            "isAdmin": "True",
            "username": "",
            "phoneNumber": "123456789",
            "password": "ak?,T4.jj12kjn@"
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
        self.comment = {
            "comment": "This is a comment"
        }
        # Initialize test db and create tables
        with app.app_context():
            self.test_db = DBOps.send_con()

    def signup(self):
        response = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user), content_type="application/json"
        )
        return response

    def invalid_password_signup(self):
        response1 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user1), content_type="application/json")
        return response1

    def invalid_email_signup(self):
        response2 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user2), content_type="application/json")
        return response2

    def empty_firstname_signup(self):
        response3 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user3), content_type="application/json")
        return response3

    def empty_last_name_signup(self):
        response4 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user4), content_type="application/json")
        return response4

    def empty_email_signup(self):
        response5 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user5), content_type="application/json")
        return response5

    def empty_password_signup(self):
        response6 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user6), content_type="application/json")
        return response6

    def empty_username_signup(self):
        response7 = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user7), content_type="application/json")
        return response7

    def login_(self):
        response = self.client.post(
            "/api/v2/login", data=json.dumps(self.login), content_type="application/json")
        return response

    def login_wrong_username(self):
        response1 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login1), content_type="application/json")
        return response1

    def login_empty_username(self):
        response2 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login2), content_type="application/json")
        return response2

    def login_empty_password(self):
        response3 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login3), content_type="application/json")
        return response3

    def login_incorrect_password(self):
        response4 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login4), content_type="application/json")
        return response4
    def fetch_token(self):
        user_resp = self.login_()
        result = json.loads(user_resp.data.decode('utf-8'))
        token = 'Bearer ' + result["token"]
        header = {"Authorization": token}
        return header

    def user_profile(self):
        res_data = self.login_()
        response = self.client.get(
            "/api/v2/profile",
            headers={"Authorization": 'Bearer ' + json.loads(res_data.data.decode('utf-8'))['token']})
        return response
    def post_meetup(self):
        header = self.fetch_token()
        response = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup), content_type="application/json")
        return response
    def meetup_empty_topic(self):
        header = self.fetch_token()
        response1 = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup1), content_type="application/json")
        return response1
    def post_question(self):
        header = self.fetch_token()
        response = self.client.post(
            "api/v2/questions", data=json.dumps(self.question), headers=header, content_type="application/json")
        return response
        
if __name__ == "__main__":
    unittest.main()
