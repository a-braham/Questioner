""" This sets up the database """

import psycopg2, os
from flask import current_app
from app import create_app

app = create_app("config")

def init_db():
    """ Method to initialize the database """
    
    url_db = current_app.config['DATABASE_URL']
    conn = psycopg2.connect(url_db)
    cursor = conn.cursor()
    sql_file = current_app.open_resource('question.sql', mode='r')
    cursor.execute(sql_file.read())
    conn.commit()
    return conn

def connection(url):
    conn = psycopg2.connect(url)
    return conn

def test_init_db():
    """ Initialize database for test """
    conn = connection(os.getenv('DATABASE_TEST_URL'))
    destroy_db()
    cursor = conn.cursor()
    sql_file = current_app.open_resource('question.sql', mode='r')
    cursor.execute(sql_file.read())
    conn.commit()
    return conn

def destroy_db():
    """ Destroy database for test """
    test_db_url = os.getenv('DATABASE_TEST_URL')
    conn = connection(test_db_url)
    cursor = conn.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    tables = [users]
    try:
        for table in tables:
            cursor.execute(table)
        conn.commit()
    except:
        print("Destry failed")