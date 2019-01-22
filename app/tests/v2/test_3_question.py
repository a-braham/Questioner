""" Tests for questions endpoints """

from .basetest import BaseTest
import json

class TestPostQuestion(BaseTest):
    """ Test class to test Questions """
    def test_create_question(self):
        """ Method to test creating question """
        response = self.post_question()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
class TestUpvote(BaseTest):
    def test_upvote(self):
        """ Testing upvoting endpoint """
        header = self.fetch_token()
        response = self.client.patch("/api/v2/questions/1/upvote", data=json.dumps(self.vote), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
class TestDownvote(BaseTest):
    def test_downvote(self):
        """ Testing downvoting endpoint """
        header = self.fetch_token()
        response = self.client.patch("/api/v2/questions/1/downvote", data=json.dumps(self.vote), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
class TestComments(BaseTest):
    def test_comments(self):
        """ Test run to test comments endpoints """
        response = self.client.post("api/v2/questions/1/comment", data=json.dumps(self.comment), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
