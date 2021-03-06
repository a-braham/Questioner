""" Models for handling Meetup data """

from datetime import datetime, timedelta
from app.database import DBOps

MEETUPS = []
RSVPS = []

class MeetUpModel(object):
    """ A class to map meetup data and relations """

    def __init__(self):
        self.meetups = MEETUPS
        self.rsvps = RSVPS

        self.MEETUPS = DBOps.send_con()

    def create_meetup(self, topic, description, location, happening_on):
        """ A method to manipulate creation of meetups """

        created_on = datetime.now().strftime("%Y-%m-%d")
        # tags = []
        # images = []
        meetup = {
            "topic": topic,
            "description": description,
            "location": location,
            "created_on": created_on,
            "happening_on": happening_on,
        }
        cursor = self.MEETUPS.cursor()
        query = """INSERT INTO meetups (topic, description, location, created_at, happening_on) VALUES (%(topic)s, %(description)s, %(location)s, %(created_on)s, %(happening_on)s) RETURNING m_id"""
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

    def create_rsvps(self, rsvp, meetup_id, u_id):
        """ A method to create rsvp record """
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rsvp = {
            "meetup_id": meetup_id,
            "u_id": u_id,
            "rsvp": rsvp,
            "created_at": created_at
        }
        cursor = self.MEETUPS.cursor()
        query = """INSERT INTO rsvp (meetup_id, u_id, rsvp, created_at) VALUES (%(meetup_id)s, %(u_id)s, %(rsvp)s, %(created_at)s) RETURNING r_id"""
        cursor.execute(query, rsvp)
        rs = cursor.fetchone()
        self.MEETUPS.commit()
        cursor.close()
        return rs
    def count_rsvp(self, mid):
        """ A method to view one meetup """
        cursor = self.MEETUPS.cursor()
        cursor.execute(
            """SELECT COUNT(r_id) FROM rsvp WHERE rsvp = 'yes' and meetup_id = '%s'""" % (mid)
        )
        rsvps = cursor.fetchall()
        cursor.close()
        return rsvps

    def search_rsvp(self, mid, uid):
        """ A method to view one meetup """
        cursor = self.MEETUPS.cursor()
        cursor.execute(
            """SELECT * FROM rsvp WHERE meetup_id = '%s' AND u_id = '%s'""" % (mid, uid)
        )
        rsvps = cursor.fetchone()
        cursor.close()
        return rsvps

    def update_rsvp(self, rsvp, mid, uid):
        """ A method to view one meetup """
        cursor = self.MEETUPS.cursor()
        cursor.execute(
            """UPDATE rsvp set rsvp = '%s' WHERE meetup_id = '%s' AND u_id = '%s' RETURNING rsvp;""" % (rsvp, mid, uid)
        )
        rsvps = cursor.fetchone()[0]
        self.MEETUPS.commit()
        cursor.close()
        return rsvps


    def create_tags(self, tags, meetup_id):
        """ A method to create rsvp record """
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tag = {
            "meetup_id": meetup_id,
            "tags": tags,
            "created_at": created_at
        }
        cursor = self.MEETUPS.cursor()
        query = """INSERT INTO tags (meetup_id, tags, created_at) VALUES (%(meetup_id)s, %(tags)s, %(created_at)s) RETURNING t_id"""
        cursor.execute(query, tag)
        tag = cursor.fetchone()
        self.MEETUPS.commit()
        cursor.close()
        return tag

    def delete_meetup(self, m_id):
        """ A method to delete meetup record """
        try:
            cursor = self.MEETUPS.cursor()
            cursor.execute(
                """DELETE FROM meetups WHERE m_id = '%s'""" % (m_id)
            )
            self.MEETUPS.commit()
            cursor.close()
            return ("Meetup deleted!!")
        except Exception as e:
            return "Cannot delete meetup", str(e)