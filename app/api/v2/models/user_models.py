""" This model hadles users """

from datetime import datetime, timedelta
import os, jwt
from instance.config import Config
from app.database import init_db

USERS = []
SECRET_KEY = Config.SECRET_KEY
token = {}

class UserModel(object):
    """ A class that maps user data """
    
    def __init__(self):
        self.DB = init_db()
        self.users = USERS
    
    def generate_auth_token(self, username):
        """ Generate auth token """
        try:
            payload = {'exp': datetime.utcnow() + timedelta(days=0, seconds=120), 'iat': datetime.utcnow(), 'sub': username}
            return jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        except Exception as e:
            return e

    def verify_auth_token(self, auth_token):
        """Verify auth token """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token exppired, login again'
        except jwt.InvalidTokenError:
            return 'Invalid token, login'
    
    def signup(self, firstname, lastname, othername, email, phoneNumber, username, isAdmin, password):
        """ Method to manipulate addition of new users into the database"""

        user = {
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "username": username,
            "email": email,
            "phoneNumber": phoneNumber,
            "isAdmin": isAdmin,
            "password": password
        }

        cursor = self.DB.cursor()
        query = """INSERT INTO users (firstname, lastname, othername, username, email, phone, isAdmin, password) VALUES (%(firstname)s, %(lastname)s, %(lastname)s, %(username)s, %(email)s, %(phoneNumber)s, %(isAdmin)s, %(password)s) RETURNING u_id"""
        cursor.execute(query, user)
        user = cursor.fetchone()[0]
        self.DB.commit()
        cursor.close()
        return user

    def login(self, username):
        """ Get user by using username """
        cursor = self.DB.cursor()
        cursor.execute(
            """SELECT username, password FROM users WHERE username = '%s'""" % (username)
        )
        user = cursor.fetchone()
        cursor.close()
        return user
        
    def get_users(self):
        """ Getting user records """
        return self.users