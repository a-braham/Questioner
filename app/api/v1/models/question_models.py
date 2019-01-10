""" Models for handling Questions data """

from datetime import datetime, timedelta

QUESTIONS = []

class QuestionModel(object):
    """ A class to map questions data and relations """

    def __init__(self):
        self.questions = QUESTIONS

    def create_question(self, title, body, meetup, createdby, votes):
        """ A method to manipulate creation of questions """

        createdOn = datetime.now()
        votes = 0
        # tags = []
        # images = []
        meetup = {
            "id": len(self.questions) + 1,
            "title": title,
            "body": body,
            "meetup": meetup,
            "createdby": createdby,
            "createdon": createdOn,
            "votes": votes
        }

        self.questions.append(meetup)
        return meetup

    def oneQuestion(self, id):
        """ method to manipulate one question data """
        
        return [question for question in self.questions if question["id"] == id]