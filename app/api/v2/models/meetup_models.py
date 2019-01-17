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
        if len(self.meetups) == 0:
            return ({
                "message": "There are no meetups"
            })
        return self.meetups

    def view_one_meetup(self, id):
        """ A method to view one meetup """
        return [meetup for meetup in MEETUPS if meetup["id"] == id]

    def create_rsvps(self, rsvp, meetup_id):
        """ A method to create rsvp record """
        rsvp = {
            "id": len(self.meetups) + 1,
            "meetup_id": meetup_id,
            "rsvp": rsvp
        }
        self.rsvps.append(rsvp)
        return rsvp