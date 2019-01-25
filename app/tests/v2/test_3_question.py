""" Tests for questions endpoints """

from .basetest import BaseTest
import json

class TestPostQuestion(BaseTest):
    """ Test class to test Questions """
    def test_create_question(self):
        """ Method to test creating question """
        response = self.post_meetup()
        response = self.post_question()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
    def test_empty_title(self):
        response1 = self.empty_title()
        restult1 = json.loads(response1.data.decode('utf-8'))
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(restult1["status"], 400)
        self.assertEqual(restult1["message"], "Title cannot be empty")
    def test_empty_body(self):
        response1 = self.empty_body()
        restult1 = json.loads(response1.data.decode('utf-8'))
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(restult1["status"], 400)
        self.assertEqual(restult1["message"], "Body cannot be empty")

class TestViewQuestion(BaseTest):
    def test_view_question(self):
        """ Tests view posted questions """
        response = self.client.get(
            "/api/v2/questions/1", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
    def test_view_question_notfound(self):
        """ Tests view posted questions not found """
        response = self.client.get(
            "/api/v2/questions/10", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["status"], 404)

class TestVote(BaseTest):
    def test_upvote(self):
        """ Testing upvoting endpoint """
        header = self.fetch_token()
        response = self.client.patch("/api/v2/questions/1/upvote", data=json.dumps(self.vote), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
    def test_downvote(self):
        """ Testing downvoting endpoint """
        header = self.fetch_token()
        response = self.client.patch("/api/v2/questions/1/downvote", data=json.dumps(self.vote), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
    def test_vote_question_notagain(self):
        """ Tests view posted questions not found """
        header = self.fetch_token()
        response = self.client.patch(
            "/api/v2/questions/1/upvote", headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
    def test_vote_question_notfound(self):
        """ Tests view posted questions not found """
        header = self.fetch_token()
        response = self.client.patch(
            "/api/v2/questions/10/downvote", headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["status"], 404)
class TestComments(BaseTest):
    def test_comments(self):
        """ Test run to test comments endpoints """
        header = self.fetch_token()
        response = self.client.post("api/v2/questions/1/comment", data=json.dumps(self.comment), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
    def test_empty_comment(self):
        header = self.fetch_token()
        response = self.client.post("api/v2/questions/1/comment", data=json.dumps(self.comment1), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["message"], "Comment posted is empty")
    def test_comment_question_notfound(self):
        """ Tests view posted questions not found """
        header = self.fetch_token()
        response = self.client.post("api/v2/questions/1p/comment", data=json.dumps(self.comment1), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["status"], 404)
    
class TestDelete(BaseTest):
    """ Test deleting meetup """
    def test_delete_meetup(self):
        """ Tests view posted meetups """
        header = self.admin_token()

        response = self.client.delete(
            "/api/v2/meetups/1/delete", headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)