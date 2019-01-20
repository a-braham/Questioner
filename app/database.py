""" This sets up the database """

import psycopg2, os
from flask import current_app, Flask
from instance.config import Config, Testing
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)

def init_db():
    """ Method to initialize the database """
    with app.app_context():
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
