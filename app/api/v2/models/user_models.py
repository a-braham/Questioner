""" This model hadles users """

from datetime import datetime, timedelta
import os, jwt
from instance.config import Config
<<<<<<< HEAD
from app.database import init_db, create_admin
=======
from app.database import DBOps
>>>>>>> e5ec976250a14405053e8571ec1a631f266dc35b

USERS = []
SECRET_KEY = Config.SECRET_KEY
token = {}

class UserModel(object):
    """ A class that maps user data """
    
    def __init__(self):
<<<<<<< HEAD
        self.DB = init_db()
        self.admin = create_admin()
=======
        self.DB = DBOps.send_con()
>>>>>>> e5ec976250a14405053e8571ec1a631f266dc35b
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
            """SELECT username, password FROM users WHERE username = '%s'""" % (username)
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
