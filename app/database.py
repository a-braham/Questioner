""" This sets up the database """

import psycopg2, os
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
        users = "DROP TABLE IF EXISTS users, meetups, questions, comments, rsvp CASCADE"
        tables = [users]
        try:
            for table in tables:
                cls.cursor.execute(table)
            cls.conn.commit()
        except Exception as e:
            print("Database exception: %s" % e)
