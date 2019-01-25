""" Destroy database for test """
import psycopg2, os
def destroy_db():
    conn = psycopg2.connect(dbname='questioner_test', user='postgres', host='localhost', password='')
    cursor = conn.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    meetups = "DROP TABLE IF EXISTS meetups CASCADE"
    questions = "DROP TABLE IF EXISTS questions CASCADE"
    comments = "DROP TABLE IF EXISTS comments CASCADE"
    rsvp = "DROP TABLE IF EXISTS rsvp CASCADE"
    voters = "DROP TABLE IF EXISTS voters CASCADE"
    tags = "DROP TABLE IF EXISTS tags CASCADE"
    tables = [users, meetups, questions, comments, rsvp, voters, tags]
    try:
        for table in tables:
            cursor.execute(table)
            conn.commit()
            print(table, "Successful!")
    except Exception as e:
        print("Database exception: %s" % e)

if __name__ == '__main__':
    destroy_db()