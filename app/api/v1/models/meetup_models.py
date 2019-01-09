""" Models for handling Meetup data """

from datetime import datetime, timedelta

MEETUPS = []

class MeetUpModel(object):
    """ A class to map meetup data and relations """

    def __init__(self):
        self.meetups = MEETUPS

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