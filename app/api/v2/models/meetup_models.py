""" Models for handling Meetup data """

from datetime import datetime, timedelta
from app.database import init_db

MEETUPS = []
RSVPS = []

class MeetUpModel(object):
    """ A class to map meetup data and relations """

    def __init__(self):
        self.meetups = MEETUPS
        self.rsvps = RSVPS

        self.MEETUPS = init_db()

    def create_meetup(self, topic, location, happening_on, tags):
        """ A method to manipulate creation of meetups """

        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # tags = []
        # images = []
        meetup = {
            "topic": topic,
            "location": location,
            "created_on": created_on,
            "happening_on": happening_on,
            "tags": tags,
        }
        cursor = self.MEETUPS.cursor()
        query = """INSERT INTO meetups (topic, location, created_at, happening_on, tags) VALUES (%(topic)s, %(location)s, %(created_on)s, %(happening_on)s, %(tags)s) RETURNING m_id"""
        cursor.execute(query, meetup)
        meetup = cursor.fetchone()
        self.MEETUPS.commit()
        cursor.close()
        return meetup

    def view_meetups(self):
        """ A method to view all upoming meetups """
        date = datetime.now()
        cursor = self.MEETUPS.cursor()
        cursor.execute(
            """SELECT * FROM meetups WHERE happening_on >= '%s'""" % (date)
        )
        meetups = cursor.fetchall()
        cursor.close()
        if not meetups:
            return "There are no meetups"
        return meetups

    def view_one_meetup(self, m_id):
        """ A method to view one meetup """
        cursor = self.MEETUPS.cursor()
        cursor.execute(
            """SELECT * FROM meetups WHERE m_id = '%s'""" % (m_id)
        )
        meetup = cursor.fetchone()
        cursor.close()
        return meetup

    def create_rsvps(self, rsvp, meetup_id):
        """ A method to create rsvp record """
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rsvp = {
            "meetup_id": meetup_id,
            "rsvp": rsvp,
            "created_at": created_at
        }
        cursor = self.MEETUPS.cursor()
        query = """INSERT INTO rsvp (meetup_id, rsvp, created_at) VALUES (%(meetup_id)s, %(rsvp)s, %(created_at)s) RETURNING r_id"""
        cursor.execute(query, rsvp)
        rs = cursor.fetchone()
        self.MEETUPS.commit()
        cursor.close()
        return rs