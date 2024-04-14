from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Event
# Create your tests here.
User = get_user_model()

class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kirti', password='123')
        self.userb = User.objects.create_user(username='someone', password='somepassword2')
        Event.objects.create(content="my first event", 
            user=self.user)
        Event.objects.create(content="my first event", 
            user=self.user)
        Event.objects.create(content="my first event", 
            user=self.userb)
        self.currentCount = Event.objects.all().count()

    def test_event_created(self):
        event_obj = Event.objects.create(content="my second event", 
            user=self.user)
        self.assertEqual(event_obj.id, 4)
        self.assertEqual(event_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='123')
        return client
    
    def test_event_list(self):
        client = self.get_client()
        response = client.get("/api/events/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_list(self):
        client = self.get_client()
        response = client.get("/api/events/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/events/action/", 
            {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/events/action/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/events/action/", 
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_comment(self):
        client = self.get_client()
        response = client.post("/api/events/action/", 
            {"id": 2, "action": "comment"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_event_id = data.get("id")
        self.assertNotEqual(2, new_event_id)
        self.assertEqual(self.currentCount + 1, new_event_id)

    def test_event_create_api_view(self):
        request_data = {"content": "This is my test event"}
        client = self.get_client()
        response = client.post("/api/events/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_event_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_event_id)
    
    def test_event_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/events/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_event_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/events/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/events/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/events/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)
