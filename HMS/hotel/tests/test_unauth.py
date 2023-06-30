import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from hotel.models import Room


class UnauthTests(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

    @classmethod
    def setUpTestData(cls):
        Room.objects.create(number='101', price='1000.00', capacity=1)
        Room.objects.create(number='102', price='1500.00', capacity=2)

    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').exists(), True)

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_room_list(self):
        url = reverse('room-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_room_details(self):
        url = reverse('room-detail', kwargs={'pk': 6})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_room(self):
        url = reverse('room-list')
        data = {
            'number': '103',
            'price': '2000',
            'capacity': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_booking(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_booking(self):
        url = reverse('booking-list')
        data = {
            "check_in": "2023-07-01",
            "check_out": "2023-07-08",
            "user": 2,
            "room": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)