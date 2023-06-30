import datetime
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from hotel.models import Room


class AdminTests(APITestCase):

    def setUp(self) -> None:
        self.my_admin = User(username='atakashi', is_staff=True)
        self.my_admin.set_password('pass_word')
        self.my_admin.save()
        loginresponse = self.client.login(username='atakashi', password='pass_word')
        self.assertTrue(loginresponse)

    @classmethod
    def setUpTestData(cls):
        Room.objects.create(number='101', price='1000.00', capacity=1)
        Room.objects.create(number='102', price='1500.00', capacity=2)

    def test_post_room(self):
        url = reverse('room-list')
        data = {
            'number': '103',
            'price': '2000',
            'capacity': 1
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_room(self):
        url = reverse('room-detail', kwargs={'pk': 2})
        data = {
            'number': '103',
            'price': '2500',
            'capacity': 2
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_booking(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_booking(self):
        url = reverse('booking-list')
        data = {
            "check_in": "2023-07-01",
            "check_out": "2023-07-08",
            "user": 2,
            "room": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
