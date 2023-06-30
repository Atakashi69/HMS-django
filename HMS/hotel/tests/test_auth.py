from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from hotel.models import Room


class AuthTests(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='user1', password='pass1')
        self.test_user.save()
        loginresponse = self.client.login(username='user1', password='pass1')
        self.assertTrue(loginresponse)

    @classmethod
    def setUpTestData(cls):
        Room.objects.create(number='101', price='1000.00', capacity=1)
        Room.objects.create(number='102', price='1500.00', capacity=2)

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            'username': 'user1',
            'password': 'pass1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_booking(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_bad_booking(self):
        url = reverse('booking-list')
        data = {
            "check_in": "2023-07-01",
            "check_out": "2023-07-08",
            "user": 2,
            "room": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_booking(self):
        url = reverse('booking-list')
        data = {
            "check_in": "2023-07-01",
            "check_out": "2023-07-08",
            "user": self.test_user.id,
            "room": 4
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)