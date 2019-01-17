""" Models for handling Questions data """

from datetime import datetime, timedelta
from app.database import init_db

QUESTIONS = []


class QuestionModel(object):
    """ A class to map questions data and relations """

    def __init__(self):
        self.questions = QUESTIONS
        self.DB = init_db()

    def create_question(self, title, body, meetup, createdby, votes):
        """ A method to manipulate creation of questions """

        createdon = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        votes = 0

        question = {
            "title": title,
            "body": body,
            "meetup": meetup,
            "createdby": createdby,
            "createdon": createdon,
            "votes": votes
        }

        cursor = self.DB.cursor()
        query = """INSERT INTO questions (title, body, meetup, created_by, created_at, votes) VALUES (%(title)s, %(body)s, %(meetup)s, %(createdby)s, %(createdon)s, %(votes)s) RETURNING q_id"""
        cursor.execute(query, question)
        question = cursor.fetchone()
        self.DB.commit()
        cursor.close()
        return question

    def oneQuestion(self, qid):
        """ method to manipulate one question data """
        cursor = self.DB.cursor()
        cursor.execute(
            """SELECT * FROM questions WHERE q_id = '%s'""" % (qid)
        )
        question = cursor.fetchone()
        cursor.close()
        return question

    def upVote(self, qid, vote):
        """ method to manipulate one question voting """
        cursor = self.DB.cursor()
        cursor.execute("""UPDATE questions SET votes = votes + %d WHERE q_id = %d RETURNING votes;""" % (vote, int(qid)))
        data = cursor.fetchone()[0]
        self.DB.commit()
        cursor.close()
        return data

    def downVote(self, qid, vote):
        """ method to manipulate one question voting """
        cursor = self.DB.cursor()
        cursor.execute("""UPDATE questions SET votes = votes - %d WHERE q_id = %d RETURNING votes;""" % (vote, int(qid)))
        data = cursor.fetchone()[0]
        self.DB.commit()
        cursor.close()
        return data
