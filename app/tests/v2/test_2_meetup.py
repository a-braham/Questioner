from .basetest import BaseTest
import json

class TestPostMeetup(BaseTest):
    """Test class for meetup views """
    def test_create_meetup(self):
        """ Test creation of meetup """
        response = self.post_meetup()
        restult = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(restult["status"], 201)
    def test_empty_topic(self):
        response1 = self.meetup_empty_topic()
        restult1 = json.loads(response1.data.decode('utf-8'))
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(restult1["status"], 400)
        self.assertEqual(restult1["message"], "Topic cannot be empty")

class TestViewMeetup(BaseTest):
    def test_view_meetup(self):
        """ Tests view posted meetups """
        response = self.client.get(
            "/api/v2/meetups/upcoming", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

    def test_view_one_meetup(self):
        """ Tests view posted meetups """
        response = self.client.get(
            "/api/v2/meetups/1", content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)

class TestRspvs(BaseTest):
    def test_create_rsvp(self):
        """ Tests view posted meetups """
        header = self.fetch_token()
        response = self.client.post(
            "/api/v2/meetups/1/rsvps", data=json.dumps(self.rsvp), headers=header, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        