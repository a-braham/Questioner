""" Test for User endpoints """
from .basetest import BaseTest
import json
class TestSignup(BaseTest):
    """Test case class for testing user data for signup"""
    def test_user_signup(self):
        """ Test signup user """
        response = self.signup()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)

    def test_invalid_password(self):
        response1 = self.invalid_password_signup()
        result1 = json.loads(response1.data.decode('utf-8'))
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(result1["status"], 400)
        self.assertEqual(result1["message"], "Password not valid")

    def test_invalid_email(self):
        response2 = self.invalid_email_signup()
        result2 = json.loads(response2.data.decode('utf-8'))

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(result2["status"], 400)
        self.assertEqual(result2["message"], "Invalid email")

    def test_firstname_signup(self):
        response3 = self.empty_firstname_signup()
        result3 = json.loads(response3.data.decode('utf-8'))

        self.assertEqual(response3.status_code, 400)
        self.assertEqual(result3["status"], 400)
        self.assertEqual(result3["message"], "Firstname is required")

    def test_lastname_signup(self):
        response4 = self.empty_last_name_signup()
        result4 = json.loads(response4.data.decode('utf-8'))

        self.assertEqual(response4.status_code, 400)
        self.assertEqual(result4["status"], 400)
        self.assertEqual(result4["message"], "Lastname is required")

    def test_email_signup(self):
        response5 = self.empty_email_signup()
        result5 = json.loads(response5.data.decode('utf-8'))

        self.assertEqual(response5.status_code, 400)
        self.assertEqual(result5["status"], 400)
        self.assertEqual(result5["message"], "email is required")

    def test_password_signup(self):
        response6 = self.empty_password_signup()
        result6 = json.loads(response6.data.decode('utf-8'))

        self.assertEqual(response6.status_code, 400)
        self.assertEqual(result6["status"], 400)
        self.assertEqual(result6["message"], "Password is required")
    
    def test_username_signup(self):
        response7 = self.empty_username_signup()
        result7 = json.loads(response7.data.decode('utf-8'))
        self.assertEqual(response7.status_code, 400)
        self.assertEqual(result7["status"], 400)
        self.assertEqual(result7["message"], "Username is required")
class TestUsers(BaseTest):
    """Test case class for testing user data for login"""
    def test_get_users(self):
        """ Tests view posted meetups """
        response = self.client.get(
            "/api/v2/get_users", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

class TestLogin(BaseTest):
    """Test case class for testing user data for login"""
    def test_user_login(self):
        """ Test login user """
        response = self.login_()
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        self.assertTrue(result["token"])

    def test_wrong_username(self):
        response1 = self.login_wrong_username()
        result1 = json.loads(response1.data.decode('utf-8'))

        self.assertEqual(response1.status_code, 404)
        self.assertEqual(result1["status"], 404)
        self.assertEqual(result1["message"], "User does not exist")

    def test_empty_login_username(self):
        response2 = self.login_empty_username()
        result2 = json.loads(response2.data.decode('utf-8'))

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(result2["status"], 400)
        self.assertEqual(result2["message"], "Username is required")

    def test_empty_login_password(self):
        response3 = self.login_empty_password()
        result3 = json.loads(response3.data.decode('utf-8'))

        self.assertEqual(response3.status_code, 400)
        self.assertEqual(result3["status"], 400)
        self.assertEqual(result3["message"], "Password is required")

    def test_incorrect_password(self):
        response4 = self.login_incorrect_password()
        result4 = json.loads(response4.data.decode('utf-8'))

        self.assertEqual(response4.status_code, 400)
        self.assertEqual(result4["status"], 400)
        self.assertEqual(result4["message"], "Incorrect password")

class TestProfile(BaseTest):
    """Test case class for testing user data for login"""
    def test_user_profile(self):
        response = self.user_profile()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)