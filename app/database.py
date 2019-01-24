""" This sets up the database """

import psycopg2, os
from flask import current_app, Flask
from instance.config import Config, Testing
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import current_app

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
        users = "DROP TABLE IF EXISTS users CASCADE"
        meetups = "DROP TABLE IF EXISTS meetups CASCADE"
        questions = "DROP TABLE IF EXISTS questions CASCADE"
        comments = "DROP TABLE IF EXISTS comments CASCADE"
        rsvp = "DROP TABLE IF EXISTS rsvp CASCADE"
        tags = "DROP TABLE IF EXISTS tags CASCADE"
        tables = [users, meetups, questions, comments, rsvp, tags]
        try:
            for table in tables:
                cls.cursor.execute(table)
                cls.conn.commit()
        except Exception as e:
            print("Database exception: %s" % e)
    @classmethod
    def create_admin(cls):
        """ Method to manipulate addition of new users into the database"""
        username = "admin"
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute(
                """SELECT * FROM users WHERE username = '%s'""" % (username)
            )
        cls.user = cls.cursor.fetchone()
        if not cls.user:
            firstname="admin"
            lastname="admin"
            othername="admin"
            email="admin@gmail.com"
            phone="07100000"
            username="admin"
            password=generate_password_hash("super", method='pbkdf2:sha256', salt_length=8)
            isAdmin = 1
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cls.user = {
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
            cls.query = """INSERT INTO users (firstname, lastname, othername, username, email, phone, isAdmin, password, created_at) VALUES (%(firstname)s, %(lastname)s, %(lastname)s, %(username)s, %(email)s, %(phone)s, %(isAdmin)s, %(password)s, %(created_at)s) RETURNING u_id"""
            cls.cursor.execute(cls.query, cls.user)
            cls.user = cls.cursor.fetchone()[0]
            cls.conn.commit()
            cls.cursor.close()
            return cls.user
