from datetime import datetime

import django_filters
from .models import Room, Booking
from hotel.booking_functions.availability import check_availability


class RoomAvailabilityFilter(django_filters.BaseInFilter):
    def filter(self, qs, value):
        check_in, check_out = value.split(',')
        check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out, '%Y-%m-%d').date()

        available_rooms = []
        for room in qs:
            if check_availability(room, check_in, check_out):
                available_rooms.append(room.id)
        return available_rooms

class RoomFilter(django_filters.FilterSet):
    availability = django_filters.CharFilter(method='filter_availability')
    class Meta:
        model = Room
        fields = {
            'number': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'capacity': ['exact', 'gte', 'lte'],
        }

    def filter_availability(self, queryset, name, value):
        return queryset.filter(id__in=RoomAvailabilityFilter().filter(queryset, value))


class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'user': ['exact'],
            'room': ['exact'],
            'check_in': ['exact', 'gte', 'lte'],
            'check_out': ['exact', 'gte', 'lte'],
        }