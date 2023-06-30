import django_filters
from .models import Room, Booking

class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'number': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'capacity': ['exact', 'gte', 'lte'],
        }

class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'user': ['exact'],
            'room': ['exact'],
            'check_in': ['exact', 'gte', 'lte'],
            'check_out': ['exact', 'gte', 'lte'],
        }