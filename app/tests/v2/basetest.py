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
            "firstname": "Cyrus",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "cyrus@gmail.com",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": "@0x.b6pV"
        }
        self.user1 = {
            "firstname": "Cyrus",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "cyrus@gmail.com",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": "qwerty"
        }
        self.user2 = {
            "firstname": "Cyrus",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "cyrgmail.com",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": "@0x.b6pV"
        }
        self.user3 = {
            "firstname": "",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "cyrus@gmail.com",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": "@0x.b6pV"
        }
        self.user4 = {
            "firstname": "Cyrus",
            "lastname": "",
            "othername": "Kamau",
            "email": "cyrus@gmail.com",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": "@0x.b6pV"
        }
        self.user5 = {
            "firstname": "Cyrus",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": "@0x.b6pV"
        }
        self.user6 = {
            "firstname": "Cyrus",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "cyrus@gmail.com",
            "phoneNumber": "123456789",
            "username": "cyro",
            "password": ""
        }
        self.user7 = {
            "firstname": "Cyrus",
            "lastname": "Kariuki",
            "othername": "Kamau",
            "email": "cyrus@gmail.com",
            "phoneNumber": "123456789",
            "username": "",
            "password": "@0x.b6pV"
        }

        self.login = {
            "username": "cyro",
            "password": "@0x.b6pV"
        }
        self.admin = {
            "username": "admin",
            "password": "super"
        }
        self.login1 = {
            "username": "Kama",
            "password": "@0x.b6pV"
        }
        self.login2 = {
            "username": "",
            "password": "@0x.b6pV"
        }
        self.login3 = {
            "username": "cyro",
            "password": ""
        }
        self.login4 = {
            "username": "cyro",
            "password": "hfkhkblllbkjvhcc"
        }
        self.meetup = {
            "topic": "Python",
            "description": "Welcome to Westmasters first Open House. During this Valentine themed special meeting, you have a chance to learn, experience and interact with all things Toastmasters. Westmasters is a Toastmasters club that is part of Toastmasters International, the world wide leader in communication and leadership development.Westmasters offers a unique opportunity to people working or residing in Westlands to improve their confidence and competence in public speaking in a fun and friendly environment. Join us for this Open House meeting where members practice speaking in front of others and afterwards receive positive and helpful evaluations. Choose to take part in an impromptu speaking session that lets you gain in confidence speaking on short notice. Hear testimonies from Toastmasters who have gained from the program and get the chance to ask questions. Meet like minded people happy and ready to help you grow in your journey of self improvement. Westmasters is open to all persons over the age of 18. Our meetings are well structured and always start and end on time. We meet on the 3rd Floor, Nomad Lounge, Misha Towers, Westlands Road, Nairobi. Parking is available. There is a Sh.300 meeting fee which you can pay with cash or mpesa on the day of the meeting. Other than that just come ready to learn and enjoy yourself.",
            "location": "Nairobi",
            "happeningOn": "2019-05-03"
        }
        self.meetup1 = {
            "topic": " ",
            "location": "Nairobi",
            "happeningOn": "2019-02-30",
        }
        self.meetup2 = {
            "topic": "Python",
            "location": "",
            "happeningOn": "2019-01-25"
        }
        self.meetup3 = {
            "topic": "Python",
            "location": "Nairobi",
            "happeningOn": ""
        }
        self.meetup4 = {
            "topic": "Python",
            "location": "Nairobi",
            "happeningOn": "2019-01-25 12:54:43"
        }
        self.meetup5 = {
            "topic": "Python",
            "location": "Nairobi",
            "happeningOn": "2019-01-22"
        }
        self.rsvp = {
            "rsvp": "yes",
        }
        self.tags = {
            "tags": ["Python", "Django"]
        }
        self.rsvp1 = {
            "rsvp": "yes22",
        }
        self.question = {
            "title": "Man",
            "body": "Not Hot",
        }
        self.question1 = {
            "title": "",
            "body": "Not Hot"
        }
        self.question2 = {
            "title": "Man",
            "body": ""
        }
        self.vote = {
            "votes": 1
        }
        self.comment = {
            "comment": "This is a comment"
        }
        self.comment1 = {
            "comment": ""
        }
        # Initialize test db and create tables
        with app.app_context():
            self.test_db = DBOps.send_con()

    def signup(self):
        response = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user), content_type="application/json"
        )
        return response

    def invalid_password_signup(self):
        response1 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user1), content_type="application/json")
        return response1

    def invalid_email_signup(self):
        response2 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user2), content_type="application/json")
        return response2

    def empty_firstname_signup(self):
        response3 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user3), content_type="application/json")
        return response3

    def empty_last_name_signup(self):
        response4 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user4), content_type="application/json")
        return response4

    def empty_email_signup(self):
        response5 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user5), content_type="application/json")
        return response5

    def empty_password_signup(self):
        response6 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user6), content_type="application/json")
        return response6

    def empty_username_signup(self):
        response7 = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.user7), content_type="application/json")
        return response7

    def login_(self):
        response = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.login), content_type="application/json")
        return response
    
    def login_admin(self):
        response = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.admin), content_type="application/json")
        return response

    def login_wrong_username(self):
        response1 = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.login1), content_type="application/json")
        return response1

    def login_empty_username(self):
        response2 = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.login2), content_type="application/json")
        return response2

    def login_empty_password(self):
        response3 = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.login3), content_type="application/json")
        return response3

    def login_incorrect_password(self):
        response4 = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.login4), content_type="application/json")
        return response4
    def fetch_token(self):
        user_resp = self.login_()
        result = json.loads(user_resp.data.decode('utf-8'))
        token = result["token"]
        header = {"Authorization": token}
        return header

    def admin_token(self):
        user_resp = self.login_admin()
        result = json.loads(user_resp.data.decode('utf-8'))
        token = result["token"]
        header = {"Authorization": token}
        return header

    def user_profile(self):
        res_data = self.login_()
        response = self.client.get(
            "/api/v2/profile",
            headers={"Authorization": json.loads(res_data.data.decode('utf-8'))['token']})
        return response
    def post_meetup(self):
        header = self.admin_token()
        response = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup), content_type="application/json")
        return response
    def meetup_empty_topic(self):
        header = self.admin_token()
        response1 = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup1), content_type="application/json")
        return response1
    def meetup_empty_location(self):
        header = self.admin_token()
        response1 = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup2), content_type="application/json")
        return response1
    def meetup_empty_date(self):
        header = self.admin_token()
        response1 = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup3), content_type="application/json")
        return response1
    def invalid_date_format(self):
        header = self.admin_token()
        response1 = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup4), content_type="application/json")
        return response1
    def invalid_date_time(self):
        header = self.admin_token()
        response1 = self.client.post(
            "/api/v2/meetups",
            headers=header,
            data=json.dumps(self.meetup5), content_type="application/json")
        return response1
    def post_question(self):
        header = self.fetch_token()
        response = self.client.post(
            "api/v2/meetup/1/question", data=json.dumps(self.question), headers=header, content_type="application/json")
        return response
    def empty_title(self):
        header = self.fetch_token()
        response1 = self.client.post(
            "/api/v2/meetup/1/question",
            headers=header,
            data=json.dumps(self.question1), content_type="application/json")
        return response1
    def empty_body(self):
        header = self.fetch_token()
        response1 = self.client.post(
            "/api/v2/meetup/1/question",
            headers=header,
            data=json.dumps(self.question2), content_type="application/json")
        return response1
        
if __name__ == "__main__":
    unittest.main()
