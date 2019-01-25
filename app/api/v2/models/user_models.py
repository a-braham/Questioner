""" This model hadles users """

from datetime import datetime, timedelta
import os, jwt
from instance.config import Config
from app.database import DBOps

USERS = []
SECRET_KEY = Config.SECRET_KEY
token = {}

class UserModel(object):
    """ A class that maps user data """
    
    def __init__(self):
        self.DB = DBOps.send_con()
        self.users = USERS

    
    def generate_auth_token(self, username):
        """ Generate auth token """
        try:
            payload = {'exp': datetime.utcnow() + timedelta(days=0, seconds=12000), 'iat': datetime.utcnow(), 'sub': username}
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
    
    def signup(self, firstname, lastname, othername, email, phone, username, password):
        """ Method to manipulate addition of new users into the database"""
        isAdmin = 0
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = {
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "username": username,
            "email": email,
            "phone": phone,
            "isAdmin": isAdmin,
            "password": password,
            "created_at": created_at
        }

        cursor = self.DB.cursor()
        query = """INSERT INTO users (firstname, lastname, othername, username, email, phone, isAdmin, password, created_at) VALUES (%(firstname)s, %(lastname)s, %(lastname)s, %(username)s, %(email)s, %(phone)s, %(isAdmin)s, %(password)s, %(created_at)s) RETURNING u_id"""
        cursor.execute(query, user)
        user = cursor.fetchone()[0]
        self.DB.commit()
        cursor.close()
        return user

    def login(self, username):
        """ Get user by using username """
        cursor = self.DB.cursor()
        cursor.execute(
            """SELECT username, password, u_id FROM users WHERE username = '%s'""" % (username)
        )
        user = cursor.fetchone()
        cursor.close()
        return user
        
    def get_users(self):
        """ Getting user records """
        cursor = self.DB.cursor()
        cursor.execute(
            """SELECT * FROM users"""
        )
        users = cursor.fetchall()
        return users

    def selectAdmin(self, username):
        """A method that helps search is user is admin"""
        isadmin = 1
        cursor = self.DB.cursor()
        cursor.execute(
            """SELECT * FROM users WHERE username = '%s' AND isadmin = %d""" %(username, isadmin)
        )
        user = cursor.fetchone()
        cursor.close()
        return user

    def blacklist(self, token):
        """ Method to manipulate addition of new users into the database"""
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        b_token = {
            "token": token,
            "created_at": created_at
        }

        cursor = self.DB.cursor()
        query = """INSERT INTO blascklist (token, created_at) VALUES (%(token)s, %(created_at)s) RETURNING b_id"""
        cursor.execute(query, b_token)
        user = cursor.fetchone()[0]
        self.DB.commit()
        cursor.close()
        return user