""" Models for handling Meetup data """

from datetime import datetime, timedelta

MEETUPS = []
RSVPS = []

class MeetUpModel(object):
    """ A class to map meetup data and relations """

    def __init__(self):
        self.meetups = MEETUPS
        self.rsvps = RSVPS

    def create_meetup(self, topic, location, images, happeningOn, tags):
        """ A method to manipulate creation of meetups """

        createdOn = datetime.now()
        # tags = []
        # images = []
        meetup = {
            "id": len(self.meetups) + 1,
            "topic": topic,
            "location": location,
            "createdOn": createdOn,
            "happeningOn": happeningOn,
            "images": images,
            "tags": tags,
        }

        self.meetups.append(meetup)
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