""" This sets up the database """

import psycopg2, os
<<<<<<< HEAD
from flask import current_app, Flask
from instance.config import Config, Testing
from datetime import datetime
from werkzeug.security import generate_password_hash
=======
from flask import current_app
>>>>>>> e5ec976250a14405053e8571ec1a631f266dc35b

class DBOps:
    @classmethod
    def connect_to(cls, url):
        cls.conn = psycopg2.connect(url)

    @classmethod
    def send_con(cls):
        cls.cursor = cls.conn.cursor()
        return cls.conn

    @classmethod
    def init_db(cls):
        """ Method to initialize the database """
        try:
            cls.cursor = cls.conn.cursor()
            sql = current_app.open_resource('questioner.sql', mode='r')
            cls.cursor.execute(sql.read())
            cls.conn.commit()
            cls.cursor.close()
            return cls.conn
        except Exception as e:
            return("Database exception: %s" % e)

    @classmethod
    def destroy_db(cls):
        """ Destroy database for test """
        cls.cursor = cls.conn.cursor()
        users = "DROP TABLE IF EXISTS users, meetups, questions, comments, rsvp CASCADE"
        tables = [users]
        try:
            for table in tables:
                cls.cursor.execute(table)
            cls.conn.commit()
            return cls.conn
        except Exception as e:
            print("Database exception: %s" % e)

def create_admin():
    """ Method to manipulate addition of new users into the database"""
    db = init_db()
    username = "admin"
    cursor = db.cursor()
    cursor.execute(
            """SELECT * FROM users WHERE username = '%s'""" % (username)
        )
    user = cursor.fetchone()
    if not user:
        firstname="admin"
        lastname="admin"
        othername="admin"
        email="admin@gmail.com"
        phone="07100000"
        username="admin"
        password=generate_password_hash("super", method='pbkdf2:sha256', salt_length=8)
        isAdmin = 1
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
        query = """INSERT INTO users (firstname, lastname, othername, username, email, phone, isAdmin, password, created_at) VALUES (%(firstname)s, %(lastname)s, %(lastname)s, %(username)s, %(email)s, %(phone)s, %(isAdmin)s, %(password)s, %(created_at)s) RETURNING u_id"""
        cursor.execute(query, user)
        user = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        return user
