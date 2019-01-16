""" This sets up the database """

import psycopg2, os
from flask import current_app, Flask
from instance.config import Config, Testing

app = Flask(__name__)

def init_db():
    """ Method to initialize the database """
    with app.app_context():
        # conn = psycopg2.connect(dbname='Questioner', user='postgres', host='localhost', password='')
        url_db = Config.DATABASE_URL
        conn = psycopg2.connect(url_db)
        cursor = conn.cursor()
        sql = current_app.open_resource('questioner.sql', mode='r')
        cursor.execute(sql.read())
        conn.commit()
        return conn

def connect_to(url):
    conn = psycopg2.connect(url)
    return conn

def _init_db():
    """ Initialize database for test """
    with app.app_context():
        # conn = psycopg2.connect(dbname='Questioner_Test', user='postgres', host='localhost', password='')
        conn = connect_to(Testing.DATABASE_TEST_URL)
        destroy_db()
        cursor = conn.cursor()
        sql_file = current_app.open_resource('questioner.sql', mode='r')
        cursor.execute(sql_file.read())
        conn.commit()
        return conn

def destroy_db():
    """ Destroy database for test """
    with app.app_context():
        # conn = psycopg2.connect(dbname='Questioner_Test', user='postgres', host='localhost', password='')
        test_db_url = Testing.DATABASE_TEST_URL
        conn = connect_to(test_db_url)
        cursor = conn.cursor()
        users = "DROP TABLE IF EXISTS users CASCADE"
        tables = [users]
        try:
            for table in tables:
                cursor.execute(table)
            conn.commit()
        except Exception as e:
            print("Database exception: %s" % e)
